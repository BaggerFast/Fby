from django.forms import ModelForm
from main.models.ya_market.support import *


class Func:
    fields = dict()
    disabled = []

    def execute(self):
        for key in self.fields.keys():
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['placeholder'] = 'Не задано'
            if key in self.disabled or self.disable:
                self.fields[key].widget.attrs['disabled'] = 'true'

    def min_max_value(self):
        for key in self.fields.keys():
            self.fields[key].widget.attrs['min'] = 0
            self.fields[key].widget.attrs['max'] = 100000


class ShelfLifeForm(ModelForm, Func):
    def __init__(self, disable: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable = disable
        self.execute()

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
    def __init__(self, disable: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable = disable
        self.min_max_value()
        self.execute()

    class Meta:
        model = WeightDimension
        exclude = ('offer', )

    def __str__(self):
        return 'weight'


class ManufacturerCountryForm(ModelForm):
    class Meta:
        model = ManufacturerCountry
        exclude = ('offer', )


class BarcodeForm(ModelForm, Func):
    def __init__(self, disable: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable = disable
        self.execute()

    class Meta:
        model = Barcode
        exclude = ('offer', )

    def __str__(self):
        return 'barcode'


class TimingForm(ModelForm):
    class Meta:
        model = Timing
        exclude = ('offer',)


class UrlForm(ModelForm, Func):
    def __init__(self, disable: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable = disable
        self.execute()

    class Meta:
        model = Url
        exclude = ('offer', )

    def __str__(self):
        return 'url'


class OfferForm(ModelForm, Func):
    disabled = ['shopSku', 'marketSku']

    def __init__(self, disable: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable = disable
        self.execute()

    class Meta:
        model = Offer
        fields = ['name', 'category', 'vendor', 'vendorCode', 'manufacturer', 'description']

    def __str__(self):
        return 'offer'


class LogisticForm(ModelForm, Func):
    def __init__(self, disable: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable = disable
        self.execute()

    class Meta:
        model = Offer
        fields = ['transportUnitSize', 'minShipment', 'quantumOfSupply', 'deliveryDurationDays', 'boxCount']

    def __str__(self):
        return 'logistic'
