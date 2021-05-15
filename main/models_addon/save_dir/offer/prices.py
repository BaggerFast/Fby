"""Паррерн для сохранения данных о цене в БД"""

from django.core.exceptions import ObjectDoesNotExist

from main.models_addon import Offer, Price
from main.models_addon.save_dir.base import BasePattern
from main.serializers.offer_price import OfferForPriceSerializer


class PricePattern(BasePattern):
    """
    Класс сохраняющий данные price из json в БД.
    """
    MODELS = {
        Offer: {
            'unique_fields': ['shopSku', 'user'],
            'update_fields': ['marketSku', 'updatedAt']
        },
        Price: {
            'unique_fields': ['offer'],
            'update_fields': ['currencyId', 'discountBase', 'value', 'vat']
        }
    }

    def save(self, user) -> None:
        """Сохраняет цены на товары"""
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
            self.created_objects.extend(serializer.created_objs)
            self.updated_objects.extend(serializer.updated_objs)

        self.bulk_create_update()
