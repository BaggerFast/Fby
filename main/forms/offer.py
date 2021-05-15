from django import forms
from django.forms import ModelForm
from main.models_addon.ya_market.offer.support import *


class Func:
    fields = dict()
    disabled = []

    def set_disable(self, disable: bool = False):
        for key in self.fields.keys():
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['placeholder'] = 'Не задано'
            if key in self.disabled or disable:
                self.fields[key].widget.attrs['disabled'] = 'true'

    def min_max_value(self):
        for key in self.fields.keys():
            self.fields[key].widget.attrs['min'] = 0
            self.fields[key].widget.attrs['max'] = 100000


class ShelfLifeForm(ModelForm, Func):
    prefix = 'ShelfLife'

    class Meta:
        model = ShelfLife
        exclude = ('offer',)
        help_texts = {
            'timePeriod': """Через сколько дней товар станет непригоден для использования. Например, срок годности есть 
                            у таких категорий, как продукты питания и медицинские препараты.""",
            'comment': 'Дополнительные условия хранения.',
        }
        labels = {
            'timePeriod': 'Срок годности',
            'comment': 'Комментарий к сроку годности',
        }


class LifeTimeForm(ModelForm, Func):
    prefix = 'LifeTime'

    class Meta:
        model = LifeTime
        exclude = ('offer',)
        help_texts = {
            'timePeriod': """В течение какого периода товар будет исправно выполнять свою функцию, 
                            а изготовитель — нести ответственность за его существенные недостатки.""",
            'comment': 'Дополнительные условия использования в течение срока службы.',
        }
        labels = {
            'timePeriod': 'Срок службы',
            'comment': 'Комментарий к сроку службы',
        }


class GuaranteePeriodForm(ModelForm, Func):
    prefix = 'GuaranteePeriod'

    class Meta:
        model = GuaranteePeriod

        exclude = ('offer',)
        help_texts = {
            'timePeriod': """В течение этого периода возможны обслуживание и ремонт товара, возврат денег.
                                Изготовитель или продавец несет ответственность за недостатки товара.""",
            'comment': 'Дополнительные условия гарантии.',
        }
        labels = {
            'timePeriod': 'Гарантийный срок',
            'comment': 'Комментарий к гарантийному сроку',
        }


class WeightDimensionForm(ModelForm, Func):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_max_value()

    class Meta:
        model = WeightDimension
        exclude = ('offer',)


class BarcodeForm(ModelForm, Func):
    class Meta:
        model = Barcode
        exclude = ('offer',)


class ManufacturerCountryForm(ModelForm, Func):
    prefix = 'countries'

    class Meta:
        model = ManufacturerCountry
        exclude = ('offer',)


class UrlForm(ModelForm, Func):
    class Meta:
        model = Url
        exclude = ('offer',)


class OfferForm(ModelForm, Func):
    # disabled = ['shopSku', 'marketSku']
    prefix = 'offer'

    class Meta:
        model = Offer
        fields = ['name', 'shopSku', 'category', 'vendor', 'vendorCode', 'manufacturer', 'description',
                  'transportUnitSize',  'minShipment', 'quantumOfSupply', 'deliveryDurationDays', 'boxCount']
        widgets = {
            'description': forms.Textarea(),
        }


class CommodityCodeForm(ModelForm, Func):
    class Meta:
        model = CustomsCommodityCode
        exclude = ('offer',)


class PriceForm(ModelForm, Func):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_max_value()

    class Meta:
        model = Price
        exclude = ('offer',)


class AvailabilityForm(ModelForm, Func):
    class Meta:
        model = Offer
        fields = ['availability', ]
