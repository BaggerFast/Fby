from main.models import Offer, Price


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
                offer = Offer.objects.get(shopSku=item.get('id'))
            except Offer.DoesNotExist:
                continue
            price, created = Price.objects.get_or_create(offer_id=offer.id)
            for key, data in item.items():
                if key in self.keys:
                    PriceBase.Base(data=data, price=price, name=key).save()
            for key, data in item['price'].items():
                if key in self.keys:
                    PriceBase.Base(data=data, price=price, name=key).save()
            price.save()
