from django.core.exceptions import ObjectDoesNotExist

from main.models import Offer, Price
from main.models.save_dir.base import BasePattern


class PriceBase:
    """Нужен для общей категории"""
    class Base:
        def __init__(self, data, price, name=''):
            self.data = data
            self.price = price
            self.name = name

        def save(self) -> None:
            setattr(self.price, self.name, self.data)


class PricePattern(BasePattern):
    attrs = {
        'priceKeys': [
            'shopSku',
            'marketSku',
            'updatedAt',
        ],
        'priceDataKeys': [
            'currencyId',
            'vat',
            'value',
        ],
    }

    def save(self) -> None:
        for item in self.json:
            try:
                offer = Offer.objects.get(shopSku=item.get('id'))
            except ObjectDoesNotExist:
                continue
            obj, created = Price.objects.get_or_create(offer_id=offer.id)
            price = obj
            self.parse_attrs(item, price)
            price.save()

    def parse_attrs(self, item, price):
        """Парсит данные из json на 2 категории """
        for key, data in item.items():
            if key in self.attrs['priceKeys']:
                PriceBase.Base(data=data, price=price, name=key).save()
        for key, data in item['price'].items():
            if key in self.attrs['priceDataKeys']:
                PriceBase.Base(data=data, price=price.priceData, name=key).save()
