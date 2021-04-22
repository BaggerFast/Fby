"""Паррерн для сохранения отчета по товарам в БД"""

from django.core.exceptions import ObjectDoesNotExist

from main.models_addon import OfferReport, Offer, Warehouse, Stock
from main.models_addon.save_dir.base import BasePattern
from main.serializers import OfferReportSerializer, WarehouseReportSerializer


class OfferReportPattern(BasePattern):
    """
    Класс, сохраняющий отчет по остаткам товаров на складах из json в БД
    """

    @staticmethod
    def save_warehouse(data, offer: Offer) -> Warehouse:
        """Сохраняет данные по остаткам товара на складе."""
        try:
            warehouse_instance = Warehouse.objects.get(warehouse_id=data.get('id'))
            serializer = WarehouseReportSerializer(offer=offer, instance=warehouse_instance,  data=data)
        except ObjectDoesNotExist:
            serializer = WarehouseReportSerializer(offer=offer, data=data)
        if serializer.is_valid():
            warehouse = serializer.save()
        else:
            print(serializer.errors)

        return warehouse

    def save(self, user) -> None:
        """Сохраняет отчет"""
        for item in self.json:
            warehouses_data = item.pop('warehouses', [])
            try:
                offer = Offer.objects.get(shopSku=item.get('shopSku'), user=user)
            except ObjectDoesNotExist:
                continue
            try:
                instance = OfferReport.objects.get(shopSku=item.get('shopSku'), offer=offer)
                serializer = OfferReportSerializer(instance=instance, data=item)
            except ObjectDoesNotExist:
                serializer = OfferReportSerializer(data=item)

            if serializer.is_valid():
                report_instance = serializer.save(offer=offer)

                """Обновояем список актуальных складов для товара offer"""
                actual_warehouses = []
                for data_item in warehouses_data:
                    warehouse = self.save_warehouse(data_item, offer)
                    actual_warehouses.append(warehouse)
                    if warehouse not in report_instance.warehouses.all():
                        report_instance.warehouses.add(warehouse)

                """Удаляем из списка неактуальные склады"""
                for warehouse in report_instance.warehouses.all():
                    if warehouse not in actual_warehouses:
                        Stock.objects.filter(warehouse=warehouse, offer=offer).delete()
                        report_instance.warehouses.remove(warehouse)
            else:
                print(serializer.errors)
