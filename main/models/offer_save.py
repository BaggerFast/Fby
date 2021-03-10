from main.models import Offer
from main.models import Barcode, Url, ManufacturerCountry, WeightDimension, ProcessingState, SupplyScheduleDays


class OfferBase:
    class Base:
        def __init__(self, data, offer):
            self.data = data
            self.offer = offer

        def save(self):
            raise NotImplementedError

    class Name(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = str(self.data)

        def save(self):
            self.offer.name = self.data

    class ShopSku(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = str(self.data)

        def save(self):
            self.offer.shopSku = self.data

    class Category(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = str(self.data)

        def save(self):
            self.offer.category = self.data

    class Vendor(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = str(self.data)

        def save(self):
            self.offer.vendor = self.data

    class VendorCode(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = str(self.data)

        def save(self):
            self.offer.vendorCode = self.data

    class Description(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = str(self.data)

        def save(self):
            self.offer.description = self.data

    class Barcodes(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)

        def save(self):
            for item in self.data:
                Barcode(offer=self.offer, barcode=item).save()

    class Urls(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)

        def save(self):
            for item in self.data:
                Url(offer=self.offer, url=item).save()

    class Manufacturer(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = str(self.data)

        def save(self):
            self.offer.manufacturer = self.data

    class ManufacturerCountries(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)

        def save(self):
            for item in self.data:
                ManufacturerCountry(offer=self.offer, name=item).save()

    class MinShipment(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = int(self.data)

        def save(self):
            self.offer.minShipment = self.data

    class TransportUnitSize(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = int(self.data)

        def save(self):
            self.offer.transportUnitSize = self.data

    class QuantumOfSupply(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = int(self.data)

        def save(self):
            self.offer.quantumOfSupply = self.data

    class DeliveryDurationDays(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = int(self.data)

        def save(self):
            self.offer.deliveryDurationDays = self.data

    class WeightDimensions(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.length = float(self.data['length'])
            self.width = float(self.data['width'])
            self.height = float(self.data['height'])
            self.weight = float(self.data['weight'])

        def save(self):
            WeightDimension(
                offer=self.offer,
                length=self.length,
                width=self.width,
                height=self.height,
                weight=self.weight
            ).save()

    class SupplyScheduleDays(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = str(self.data)

        def save(self):
            SupplyScheduleDays(offer=self.offer, supply_schedule_day=self.data).save()

    class ProcessingState(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)

        def save(self):
            ProcessingState(offer=self.offer, status=self.data['status']).save()

    class Availability(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = str(self.data)

        def save(self):
            self.offer.availability = self.data

    class Mapping(Base):
        def pre_init(self, data, offer):
            super().__init__(data, offer)
            self.marketSku = int(self.data["marketSku"]),
            self.categoryId = int(self.data["categoryId"])

    @staticmethod
    def clear():
        Offer.objects.all().delete()


class OfferPattern:
    class_list = {
        "name": OfferBase.Name,
        "shopSku": OfferBase.ShopSku,
        "category": OfferBase.Category,
        "vendor": OfferBase.Vendor,
        "vendorCode": OfferBase.VendorCode,
        "description": OfferBase.Description,
        "barcodes": OfferBase.Barcodes,
        "urls": OfferBase.Urls,
        "manufacturer": OfferBase.Manufacturer,
        "manufacturerCountries": OfferBase.ManufacturerCountries,
        "minShipment": OfferBase.MinShipment,
        "transportUnitSize": OfferBase.TransportUnitSize,
        "quantumOfSupply": OfferBase.QuantumOfSupply,
        "deliveryDurationDays": OfferBase.DeliveryDurationDays,
        "weightDimensions": OfferBase.WeightDimensions,
        "supplyScheduleDays": OfferBase.SupplyScheduleDays,
        "processingState": OfferBase.ProcessingState,
        "availability": OfferBase.Availability,
        "mapping": OfferBase.Mapping,
    }

    def __init__(self, json):
        self.json = json
        OfferBase.clear()

    def save(self):
        for item in self.json:
            offer = Offer.objects.create()
            for key_class, data in item['offer'].items():
                self.class_list[key_class](data=data, offer=offer).save()
            offer.save()
