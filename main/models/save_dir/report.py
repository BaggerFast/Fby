from django.core.exceptions import ObjectDoesNotExist

from main.models import OfferReport, Offer, Warehouse, Stock
from main.serializers import OfferSerializer, MappingSerializer, OfferReportSerializer, StockSerializer
from main.serializers.offer_report import WarehouseReportSerializer


class OfferReportPattern:
    """
    Класс, сохраняющий отчет по остаткам товаров на складах из json в БД
    """

    def __init__(self, json):
        self.json = json

    @staticmethod
    def save_warehouse(data, offer):
        """
        Сохраняет данные по остаткам товара на складе
        """
        try:
            warehouse_instance = Warehouse.objects.get(warehouse_id=data.get('id'))
            serializer = WarehouseReportSerializer(offer=offer, instance=warehouse_instance,  data=data)
        except ObjectDoesNotExist:
            serializer = WarehouseReportSerializer(offer=offer, data=data)
        if serializer.is_valid():
            warehouse = serializer.save()
        else:
            print(serializer.errors)

        # stocks_data = data.pop('stocks', [])
        # warehouse = Warehouse.objects.get_or_create(warehouse_id=data.get('id'), name=data.get('name'))[0]
        #
        # actual_stocks = []
        # for stock_data in stocks_data:
        #     try:
        #         stock_instance = Stock.objects.get(warehouse=warehouse, offer=offer, type=stock_data.get('type'))
        #         serializer = StockSerializer(instance=stock_instance, data=stock_data)
        #     except ObjectDoesNotExist:
        #         serializer = StockSerializer(data=stock_data)
        #
        #     if serializer.is_valid():
        #         stock = serializer.save(warehouse=warehouse, offer=offer)
        #         actual_stocks.append(stock)
        #     else:
        #         print(serializer.errors)
        #
        # for stock in offer.stocks.filter(warehouse=warehouse, offer=offer):
        #     if stock not in actual_stocks:
        #         stock.delete()

        return warehouse

    def save(self, user):
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

                actual_warehouses = []
                for data_item in warehouses_data:
                    warehouse = self.save_warehouse(data_item, offer)
                    actual_warehouses.append(warehouse)
                    if warehouse not in report_instance.warehouses.all():
                        report_instance.warehouses.add(warehouse)

                for warehouse in report_instance.warehouses.all():
                    if warehouse not in actual_warehouses:
                        Stock.objects.filter(warehouse=warehouse, offer=offer).delete()
                        # offer.stocks.filter(warehouse=warehouse).delete()
                        report_instance.warehouses.remove(warehouse)
            else:
                print(serializer.errors)
