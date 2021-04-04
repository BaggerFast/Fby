from django.core.exceptions import ObjectDoesNotExist

from main.models.ya_market.order.base import Order
from main.serializers.orders import OrderSerializer


class OrderPattern:
    """Класс, сохраняющий данные order из json в БД"""

    def __init__(self, json):
        self.json = json

    def save(self):
        for item in self.json:
            try:
                instance = Order.objects.get(order_id=item.get('id'))
                serializer = OrderSerializer(instance=instance, data=item)
            except ObjectDoesNotExist:
                serializer = OrderSerializer(data=item)

            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
