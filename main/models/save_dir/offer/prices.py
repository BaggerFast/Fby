from django.core.exceptions import ObjectDoesNotExist

from main.models import Offer
from main.serializers.offer_price import OfferForPriceSerializer


class PricePattern:
    """Класс сохраняющий данные price из json в БД."""

    def __init__(self, json: dict):
        self.json = json

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
