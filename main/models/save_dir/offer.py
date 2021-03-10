from main.models import Offer
from main.models import Barcode, Url, ManufacturerCountry, WeightDimension, ProcessingState, SupplyScheduleDays, Mapping
from django.core.exceptions import ObjectDoesNotExist


class OfferBase:
    class Base:
        def __init__(self, data, offer, name=''):
            self.data = data
            self.offer = offer
            self.name = name

        def save(self):
            setattr(self.offer, self.name, self.data)

    class Barcodes(Base):
        def save(self):
            for item in self.data:
                Barcode.objects.update_or_create(offer=self.offer, barcode=item)

    class Urls(Base):
        def save(self):
            for item in self.data:
                Url(offer=self.offer, url=item).save()

    class ManufacturerCountries(Base):
        def save(self):
            for item in self.data:
                ManufacturerCountry.objects.update_or_create(offer=self.offer, name=item)

    class WeightDimensions(Base):
        def save(self):
            WeightDimension.objects.update_or_create(
                offer=self.offer,
                length=float(self.data['length']),
                width=float(self.data['width']),
                height=float(self.data['height']),
                weight=float(self.data['weight'])
            )

    class SupplyScheduleDays(Base):
        def save(self):
            SupplyScheduleDays.objects.update_or_create(offer=self.offer, supplyScheduleDay=self.data)

    class ProcessingState(Base):
        def save(self):
            ProcessingState.objects.update_or_create(offer=self.offer, status=self.data['status'])

    class Mapping(Base):
        def save(self):
            Mapping.objects.update_or_create(
                offer=self.offer,
                marketSku=self.data["marketSku"],
                categoryId=self.data["categoryId"],
            )


class OfferPattern:
    simple = [
        'name',
        'shopSku',
        'category',
        'vendor',
        'vendorCode',
        'description',
        'manufacturer',
        'minShipment',
        'transportUnitSize',
        'quantumOfSupply',
        'deliveryDurationDays',
        'availability',
    ]

    foreign = [
        "barcodes",
        "urls",
        "weightDimensions",
        "supplyScheduleDays",
        "processingState",
        "manufacturerCountries",
        "mapping",
    ]

    def __init__(self, json):
        self.json = json

    def save(self):
        for item in self.json:
            try:
                offer = Offer.objects.get(shopSku=item['offer'].get('shopSku'))
            except ObjectDoesNotExist:
                offer = Offer.objects.create()

            json_offer = item['offer']
            if 'mapping' in item:
                json_offer['mapping'] = item['mapping']

            for key, data in json_offer.items():
                if key in self.simple:
                    OfferBase.Base(data=data, offer=offer, name=key).save()
                elif key in self.foreign:
                    getattr(OfferBase, key[0].title()+key[1::])(data=data, offer=offer).save()
            offer.save()
