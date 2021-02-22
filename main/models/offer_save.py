from main.models import Offer


class OfferBase:
    class Base:
        def __init__(self, data, offer):
            self.data = data
            self.offer = offer  # использовать для foreign_key

        def save(self):
            raise NotImplementedError

        def printor(self):
            print(self.offer)

    class Name(Base):
        def save(self):
            pass

    class ShopSku(Base):
        def save(self):
            pass

    class Category(Base):
        def save(self):
            pass

    class Vendor(Base):
        def save(self):
            pass

    class VendorCode(Base):
        def save(self):
            pass

    class Description(Base):
        def save(self):
            pass

    class Barcodes(Base):
        def save(self):
            pass

    class Urls(Base):
        def save(self):
            pass

    class Manufacturer(Base):
        def save(self):
            pass

    class ManufacturerCountries(Base):
        def save(self):
            pass

    class MinShipment(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = int(self.data)

        def save(self):
            pass

    class TransportUnitSize(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = int(self.data)

        def save(self):
            pass

    class QuantumOfSupply(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = int(self.data)

        def save(self):
            pass

    class DeliveryDurationDays(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.data = int(self.data)

        def save(self):
            pass

    class WeightDimensions(Base):
        def __init__(self, data, offer):
            super().__init__(data, offer)
            self.length = float(self.data['length'])
            self.width = float(self.data['width'])
            self.height = float(self.data['height'])
            self.weight = float(self.data['weight'])

        def save(self):
            pass

    class SupplyScheduleDays(Base):
        def save(self):
            pass

    class ProcessingState(Base):
        def save(self):
            pass

    class Availability(Base):
        def save(self):
            pass

    class Mapping(Base):
        def pre_init(self, data, offer):
            super().__init__(data, offer)
            self.marketSku = int(self.data["marketSku"]),
            self.categoryId = int(self.data["categoryId"])


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

    def save(self):
        for item in self.json:
            #offer = Offer.objects.create()
            for key_class, data in item['offer'].items():
                pass
                #self.class_list[key_class](data=data, offer=offer).save()
           #offer.save()




