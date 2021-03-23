from django.forms import ModelForm, forms
from main.models.ya_market.base import Offer
from main.models.ya_market.support import WeightDimension


class WeightDimensionForm(ModelForm):
    class Meta:
        model = WeightDimension
        exclude = ('offer', )


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['shopSku', 'marketSku', 'name', 'category', 'vendor', 'vendorCode', 'manufacturer', 'description']


class LogisticForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['transportUnitSize', 'minShipment', 'quantumOfSupply', 'deliveryDurationDays', 'boxCount']
