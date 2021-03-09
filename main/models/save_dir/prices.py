from main.models import Offer, Price
from main.models.save_dir.offer import camel_to_snake


class PriceBase:
    class Base:
        def __init__(self, data, price, name=''):
            self.data = data
            self.price = price
            self.name = name

        def save(self):
            setattr(self.price, self.name, self.data)


class PricePattern:
    keys = [
        'shopSku',
        'marketSku',
        'value',
        'currencyId',
        'vat',
        'updatedAt'
    ]

    def __init__(self, json):
        self.json = json

    def save(self):
        for item in self.json:
            try:
                offer = Offer.objects.get(shop_sku=item.get('id'))
            except Offer.DoesNotExist:
                continue
            obj, created = Price.objects.get_or_create(offer_id=offer.id)
            price = obj
            for key, data in item.items():
                if key in self.keys:
                    PriceBase.Base(data=data, price=price, name=camel_to_snake(key)).save()
            for key, data in item['price'].items():
                if key in self.keys:
                    PriceBase.Base(data=data, price=price, name=camel_to_snake(key)).save()
            price.save()
