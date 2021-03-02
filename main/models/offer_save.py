from main.models import Offer
from main.models import Barcode, Url, ManufacturerCountry, WeightDimension, ProcessingState, SupplyScheduleDays


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
                Barcode(offer=self.offer, barcode=item).save()

    class Urls(Base):
        def save(self):
            for item in self.data:
                Url(offer=self.offer, url=item).save()

    class ManufacturerCountries(Base):
        def save(self):
            for item in self.data:
                ManufacturerCountry(offer=self.offer, name=item).save()

    class WeightDimensions(Base):
        def save(self):
            WeightDimension(
                offer=self.offer,
                length=float(self.data['length']),
                width=float(self.data['width']),
                height=float(self.data['height']),
                weight=float(self.data['weight'])
            ).save()

    class SupplyScheduleDays(Base):
        def save(self):
            SupplyScheduleDays(offer=self.offer, supply_schedule_day=self.data).save()

    class ProcessingState(Base):
        def save(self):
            ProcessingState(offer=self.offer, status=self.data['status']).save()

    class Mapping(Base):
        pass
            # self.marketSku = int(self.data["marketSku"]),
            # self.categoryId = int(self.data["categoryId"])

    @staticmethod
    def clear():
        Offer.objects.all().delete()


class OfferPattern:
    simple = {
        "name": 'name',
        "shopSku": 'shop_sku',
        "category": 'category',
        "vendor": 'vendor',
        "vendorCode": 'vendor_code',
        "description": 'description',
        "manufacturer": 'manufacturer',
        "minShipment": 'min_shipment',
        "transportUnitSize": 'transport_unit_size',
        "quantumOfSupply": 'quantum_of_supply',
        "deliveryDurationDays": 'delivery_duration_days',
        "availability": 'availability',
    }

    foreign = {
        "barcodes": OfferBase.Barcodes,
        "urls": OfferBase.Urls,
        "weightDimensions": OfferBase.WeightDimensions,
        "supplyScheduleDays": OfferBase.SupplyScheduleDays,
        "processingState": OfferBase.ProcessingState,
        "manufacturerCountries": OfferBase.ManufacturerCountries,
        "mapping": OfferBase.Mapping,
    }

    def __init__(self, json):
        self.json = json
        OfferBase.clear()

    def save(self):
        for item in self.json:
            offer = Offer.objects.create()
            for key, data in item['offer'].items():
                if key in self.simple.keys():
                    OfferBase.Base(data=data, offer=offer, name=self.simple[key]).save()
                elif key in self.foreign.keys():
                    self.foreign[key](data=data, offer=offer).save()
            offer.save()
