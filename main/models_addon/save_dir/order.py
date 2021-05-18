"""Паттерн для сохранения данных о заказах в БД"""

from django.core.exceptions import ObjectDoesNotExist

from main.models_addon.ya_market import Order, Commission, PaymentOrder, InitialItem, \
    Detail, ItemPrice, Payment, Item
from main.models_addon.save_dir.base import BasePattern
from main.serializers import OrderSerializer


class OrderPattern(BasePattern):
    """
    Класс, сохраняющий данные order из json в БД
    """
    MODELS = {
        Commission: {
            'unique_fields': ['order', 'type'],
            'update_fields': ['actual', 'predicted']
        },
        PaymentOrder: {
            'unique_fields': ['payment'],
            'update_fields': ['payment_order_id', 'date']
        },
        InitialItem: {
            'unique_fields': ['order', 'shopSku'],
            'update_fields': ['initialCount']
        },
        Detail: {
            'unique_fields': ['item', 'itemStatus', 'stockType'],
            'update_fields': ['itemCount', 'updateDate']
        },
        ItemPrice: {
            'unique_fields': ['item', 'type'],
            'update_fields': ['costPerItem', 'total']
        },
        Order: {
            'unique_fields': ['order_id', 'user'],
            'update_fields': ['creationDate',
                              'status',
                              'statusUpdateDate',
                              'partnerOrderId',
                              'paymentType',
                              'deliveryRegion']
        },
        Payment: {
            'unique_fields': ['order', 'type', 'source'],
            'update_fields': ['payment_id', 'date', 'total', 'paymentOrder']
        },
        Item: {
            'unique_fields': ['order', 'shopSku'],
            'update_fields': ['offerName', 'marketSku', 'count', 'warehouse']
        }
    }

    def save(self, user) -> None:
        """Сохраняет заказы"""
        for item in self.json:
            try:
                instance = Order.objects.get(order_id=item.get('id'), user=user)
                serializer = OrderSerializer(instance=instance, data=item)
            except ObjectDoesNotExist:
                serializer = OrderSerializer(data=item)
            if serializer.is_valid():
                serializer.save(user=user)
                self.created_objects.extend(serializer.created_objs)
                self.updated_objects.extend(serializer.updated_objs)
            else:
                print(serializer.errors)

        self.bulk_create_update()
