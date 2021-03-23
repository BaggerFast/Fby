from django.forms import ModelForm, forms
from main.models.ya_market.base import Offer
from main.models.ya_market.support import WeightDimension, ManufacturerCountry, Url, Barcode, Timing


class Func:
    fields = dict()
    disabled = []

    def execute(self):
        for key in self.fields.keys():
            self.fields[key].widget.attrs['class'] = 'form-control'
            if key in self.disabled or self.disable:
                self.fields[key].widget.attrs['disabled'] = 'true'


class WeightDimensionForm(ModelForm, Func):
    def __init__(self, disable=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable = disable
        self.execute()

    class Meta:
        model = WeightDimension
        exclude = ('offer', )


class ManufacturerCountryForm(ModelForm):
    class Meta:
        model = ManufacturerCountry
        exclude = ('offer', )


class BarcodeForm(ModelForm, Func):
    def __init__(self, disable=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable = disable
        self.execute()

    class Meta:
        model = Barcode
        exclude = ('offer', )


class TimingForm(ModelForm):
    class Meta:
        model = Timing
        exclude = ('offer',)


class UrlForm(ModelForm, Func):
    def __init__(self, disable=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable = disable
        self.execute()

    class Meta:
        model = Url
        exclude = ('offer', )


class OfferForm(ModelForm, Func):
    disabled = ['shopSku', 'marketSku']

    def __init__(self, disable=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable = disable
        self.execute()

    class Meta:
        model = Offer
        fields = ['shopSku', 'marketSku', 'name', 'category', 'vendor', 'vendorCode', 'manufacturer', 'description']


class LogisticForm(ModelForm, Func):
    def __init__(self, disable=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable = disable
        self.execute()

    class Meta:
        model = Offer
        fields = ['transportUnitSize', 'minShipment', 'quantumOfSupply', 'deliveryDurationDays', 'boxCount']
