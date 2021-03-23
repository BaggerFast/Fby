from django.forms import ModelForm, forms
from main.models.ya_market.base import Offer
from main.models.ya_market.support import WeightDimension, ManufacturerCountry, Url, Barcode, Timing


class WeightDimensionForm(ModelForm):
    class Meta:
        model = WeightDimension
        exclude = ('offer', )


class ManufacturerCountryForm(ModelForm):
    class Meta:
        model = ManufacturerCountry
        exclude = ('offer', )


class BarcodeForm(ModelForm):
    class Meta:
        model = Barcode
        exclude = ('offer', )


class TimingForm(ModelForm):
    class Meta:
        model = Timing
        exclude = ('offer',)


class UrlForm(ModelForm):
    class Meta:
        model = Url
        exclude = ('offer', )


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['shopSku', 'marketSku', 'name', 'category', 'vendor', 'vendorCode', 'manufacturer', 'description']


class LogisticForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['transportUnitSize', 'minShipment', 'quantumOfSupply', 'deliveryDurationDays', 'boxCount']


