"""Паррерн для сохранения отчета по товарам в БД"""

from django.core.exceptions import ObjectDoesNotExist

from main.models_addon import OfferReport, Offer, Warehouse, Stock, Hiding, Storage, Inclusion, Tariff
from main.models_addon.save_dir.base import BasePattern
from main.serializers import OfferReportSerializer, WarehouseReportSerializer


class OfferReportPattern(BasePattern):
    """
    Класс, сохраняющий отчет по остаткам товаров на складах из json в БД
    """
    MODELS = {
        OfferReport: {
            'unique_fields': ['offer', 'shopSku'],
            'update_fields': ['marketSku', 'name', 'price',
                              'categoryId', 'categoryName']
        },
        Hiding: {
            'unique_fields': ['report', 'code'],
            'update_fields': ['type', 'message', 'comment']
        },
        Storage: {
            'unique_fields': ['report', 'type'],
            'update_fields': ['count']
        },
        Inclusion: {
            'unique_fields': ['storage', 'type'],
            'update_fields': ['count']
        },
        Tariff: {
            'unique_fields': ['report', 'type'],
            'update_fields': ['percent', 'amount']
        },
        Warehouse: {
            'unique_fields': ['warehouse_id'],
            'update_fields': ['name']
        },
        Stock: {
            'unique_fields': ['warehouse', 'offer', 'type'],
            'update_fields': ['count']
        }
    }

    def save_warehouse(self, data: dict, offer: Offer) -> Warehouse:
        """Сохраняет данные по остаткам товара на складе."""
        try:
            warehouse_instance = Warehouse.objects.get(warehouse_id=data.get('id'))
            serializer = WarehouseReportSerializer(
                offer=offer,
                instance=warehouse_instance,
                data=data
            )
        except ObjectDoesNotExist:
            serializer = WarehouseReportSerializer(offer=offer, data=data)
        if serializer.is_valid():
            warehouse = serializer.save()
            self.created_objects.extend(serializer.created_objs)
            self.updated_objects.extend(serializer.updated_objs)
        else:
            print(serializer.errors)

        return warehouse

    def save(self, user) -> None:
        """Сохраняет отчет"""
        actual_reports = []
        for item in self.json:
            shop_sku = item.get('shopSku')
            name = item.get('name', '')
            warehouses_data = item.pop('warehouses', [])
            try:
                offer = Offer.objects.get(shopSku=shop_sku, user=user)
                actual_reports.append(offer)
            except ObjectDoesNotExist:
                error = f'Отчет по товару "{name}", shopSku = {shop_sku}, ' \
                        f'не сохранен, т.к. товар отсутствует в БД.'
                self.errors.append(error)
                print(error)
                continue
            try:
                instance = OfferReport.objects.get(shopSku=item.get('shopSku'), offer=offer)
                serializer = OfferReportSerializer(instance=instance, data=item)
            except ObjectDoesNotExist:
                serializer = OfferReportSerializer(data=item)

            if serializer.is_valid():
                report_instance = serializer.save(offer=offer)
                self.created_objects.extend(serializer.created_objs)
                self.updated_objects.extend(serializer.updated_objs)

                """Обновляем список актуальных складов для товара offer"""
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

        self.bulk_create_update()

        """Удаляем неактуальные отчеты"""
        report_mapping = OfferReport.objects.in_bulk(field_name='offer')
        for offer, report in report_mapping.items():
            if offer not in actual_reports:
                report.delete()
                Stock.objects.filter(offer=offer).delete()

