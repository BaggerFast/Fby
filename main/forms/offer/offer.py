from django import forms
from django.forms import ModelForm
from main.models.ya_market.offer.support import *


class Func:
    fields = dict()
    disabled = []

    def turn_off(self, disable: bool = False):
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
    class Meta:
        model = ShelfLife
        exclude = ('offer',)
        help_texts = {
            'comment': 'Дополнительные условия хранения.',
            'timePeriod': 'Через сколько дней товар станет непригоден для использования. '
                       'Например, срок годности есть у таких категорий, как продукты питания и медицинские препараты.',
        }
        labels = {
            'timePeriod': 'Срок годности',
            'comment': 'Комментарий к сроку годности',
        }

    def __str__(self):
        return 'shelfLife'


class LifeTimeForm(ShelfLifeForm):
    class Meta:
        model = ShelfLife
        exclude = ('offer',)
        help_texts = {
            'timePeriod': 'В течение этого периода возможны обслуживание и ремонт товара, возврат денег.'
                          ' Изготовитель или продавец несет ответственность за недостатки товара.',
            'comment': 'Дополнительные условия гарантии.',
        }
        labels = {
            'timePeriod': 'Гарантийный срок',
            'comment': 'Комментарий к гарантийному сроку',
        }

    def __str__(self):
        return 'lifeTime'


class GuaranteePeriodForm(ShelfLifeForm):
    class Meta:
        model = ShelfLife
        exclude = ('offer',)
        help_texts = {
            'comment': 'Дополнительные условия хранения.',
            'timePeriod': 'Через сколько дней товар станет непригоден для использования. '
                          'Например, срок годности есть у таких категорий, как продукты питания и медицинские препараты.',
        }
        labels = {
            'timePeriod': 'Срок годности',
            'comment': 'Комментарий к сроку годности',
        }

    def __str__(self):
        return 'guarantee'


class WeightDimensionForm(ModelForm, Func):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_max_value()

    class Meta:
        model = WeightDimension
        exclude = ('offer', )

    def __str__(self):
        return 'weight'


class BarcodeForm(ModelForm, Func):
    class Meta:
        model = Barcode
        exclude = ('offer', )

    def __str__(self):
        return 'barcode'


class UrlForm(ModelForm, Func):
    class Meta:
        model = Url
        exclude = ('offer', )

    def __str__(self):
        return 'url'


class OfferForm(ModelForm, Func):
    disabled = ['shopSku', 'marketSku']

    class Meta:
        model = Offer
        fields = ['name', 'category', 'vendor', 'vendorCode', 'manufacturer', 'description', 'transportUnitSize',
                  'minShipment', 'quantumOfSupply', 'deliveryDurationDays', 'boxCount']
        widgets = {
            'description': forms.Textarea(),
        }

    def __str__(self):
        return 'offer'


class CommodityCodeForm(ModelForm, Func):

    class Meta:
        model = CustomsCommodityCode
        exclude = ('offer',)

    def __str__(self):
        return 'commodityCode'


class PriceForm(ModelForm, Func):
    def __str__(self):
        return 'priceForm'

    class Meta:
        model = Price
        exclude = ('offer',)


class AvailabilityForm(ModelForm, Func):
    def __str__(self):
        return 'availabilityForm'

    class Meta:
        model = Offer
        fields = ['availability', ]
