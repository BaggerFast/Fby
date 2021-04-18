"""Паррерн для сохранения данных о цене в БД"""

from django.core.exceptions import ObjectDoesNotExist

from main.models import Offer
from main.models.save_dir.base import BasePattern
from main.serializers.offer_price import OfferForPriceSerializer


class PricePattern(BasePattern):
    """Класс сохраняющий данные price из json в БД."""

    def save(self, user) -> None:
        for item in self.json:
            try:
                instance = Offer.objects.get(shopSku=item.get('shopSku'), user=user)
                serializer = OfferForPriceSerializer(instance=instance, data=item)
            except ObjectDoesNotExist:
                continue

            if serializer.is_valid():
                serializer.save(user=user)
            else:
                print(serializer.errors)
