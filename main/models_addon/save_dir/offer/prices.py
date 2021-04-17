from django.core.exceptions import ObjectDoesNotExist

from main.models_addon import Offer as OfferModel, Price
from .offer import Base
from main.models_addon.save_dir.base import BasePattern


class Prices:
    class Price(Base):
        def save(self) -> None:
            Price.objects.update_or_create(
                offer=self.offer,
                defaults={
                    "value": self.exist("value"),
                    "vat": self.exist('vat'),
                    "discountBase": self.exist('discountBase')
                }
            )


class PricePattern(BasePattern):
    """Класс сохраняющий данные price из json в БД."""
    attrs = {
        'simple': [
            'marketSku',
            'updatedAt',

        ],
        'diff': [
            "price"
        ]
    }

    def save(self, user) -> None:
        """Сохраняет данные в БД"""
        for item in self.json:
            try:
                offer = OfferModel.objects.get(shopSku=item.get('id'), user=user)
            except ObjectDoesNotExist:
                continue
            self.parse_attrs(json=item, attr=offer, diff_class=Prices)
            offer.save()

    def parse_attrs(self, json, attr, diff_class) -> None:
        """Парсит данные из json на простые и сложные"""
        for key, data in json.items():
            if key in self.attrs['simple']:
                Base(data=data, offer=attr, name=key).save()
            elif key in self.attrs['diff']:
                getattr(diff_class, key[0].title() + key[1::])(data=data, offer=attr).save()
