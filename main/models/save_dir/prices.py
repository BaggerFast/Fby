from django.core.exceptions import ObjectDoesNotExist

from main.models import Offer, Price
from main.models.save_dir.base import BasePattern


class PriceBase:
    class Base:
        def __init__(self, data, price, name=''):
            self.data = data
            self.price = price
            self.name = name

        def save(self):
            setattr(self.price, self.name, self.data)

    @staticmethod
    def serialize_params(price, items: []):
        param = [
            'shopSku',
            'marketSku',
            'value',
            'currencyId',
            'vat',
            'updatedAt'
        ]
        for item in items:
            for key, data in item.items():
                if key in param:
                    PriceBase.Base(data=data, price=price, name=key).save()


class PricePattern(BasePattern):
    def save(self):
        for item in self.json:
            try:
                offer = Offer.objects.get(shopSku=item.get('id'))
            except ObjectDoesNotExist:
                continue
            price, created = Price.objects.get_or_create(offer_id=offer.id)
            PriceBase.serialize_params(price, [item, item['price']])
            price.save()
