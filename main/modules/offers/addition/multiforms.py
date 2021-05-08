from typing import List
from main.forms import WeightDimensionForm, UrlForm, BarcodeForm, ShelfLifeForm, LifeTimeForm, \
    GuaranteePeriodForm, CommodityCodeForm, OfferForm, PriceForm, AvailabilityForm
from main.view import FormSet


class OfferBaseFormSet(FormSet):
    def __init__(self):
        self.offer = None

    def write_foreign_key(self, instance):
        if hasattr(instance._meta.model, 'offer'):
            setattr(instance, 'offer', self.offer)
        return instance


class OfferFormSet(OfferBaseFormSet):
    def configure(self, offer=None):
        self.offer = offer
        forms_clear = [OfferForm, WeightDimensionForm, UrlForm, BarcodeForm, ShelfLifeForm,
                       LifeTimeForm, GuaranteePeriodForm, CommodityCodeForm]
        if self.offer:
            attrs = [offer, offer.weight_dimensions, offer.url, offer.barcode, offer.shelf_life,
                     offer.life_time, offer.guarantee_period, offer.commodity_codes]
        else:
            attrs = [None] * len(forms_clear)
        self.forms: list = self.cortege_from_lists(forms=forms_clear, attrs=attrs)

    def get_for_context(self) -> dict:
        print(self.get_form_list([WeightDimensionForm]))
        forms: List[List] = [
            [list(self.forms_dict[OfferForm])[:6], *self.get_form_list([UrlForm, BarcodeForm, CommodityCodeForm])],
            self.get_form_list([ShelfLifeForm, LifeTimeForm, GuaranteePeriodForm]),
            self.get_form_list([WeightDimensionForm]), [list(self.forms_dict[OfferForm])[6:]]
        ]
        accordions: list = ['Основная информация', 'Сроки', 'Габариты и вес в упаковке', 'Особенности логистики']
        return self.context(accordions=accordions, forms_context=forms)


class PriceFormSet(OfferBaseFormSet):
    def configure(self, offer=None):
        self.offer = offer
        self.forms: list = [(PriceForm, offer.get_price if offer else None),
                            (AvailabilityForm, offer if offer else None)]

    def get_for_context(self) -> dict:
        accordions: list = ['Управление ценой', 'Управление поставками']
        forms: List[list] = [self.get_form_list([PriceForm]), self.get_form_list([AvailabilityForm])]
        return self.context(accordions=accordions, forms_context=forms)
