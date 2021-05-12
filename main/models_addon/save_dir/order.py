"""Паррерн для сохранения данных о заказах в БД"""

from django.core.exceptions import ObjectDoesNotExist

from main.models_addon.ya_market import Order
from main.models_addon.save_dir.base import BasePattern
from main.serializers import OrderSerializer


class OrderPattern(BasePattern):
    """
    Класс, сохраняющий данные order из json в БД
    """

    def save(self, user):
        for item in self.json:
            try:
                instance = Order.objects.get(order_id=item.get('id'), user=user)
                serializer = OrderSerializer(instance=instance, data=item)
            except ObjectDoesNotExist:
                serializer = OrderSerializer(data=item)
            if serializer.is_valid():
                serializer.save(user=user)
            else:
                print(serializer.errors)
