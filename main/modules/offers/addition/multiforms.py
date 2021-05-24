from typing import List
from main.forms import WeightDimensionForm, UrlForm, BarcodeForm, ShelfLifeForm, LifeTimeForm, \
    GuaranteePeriodForm, CommodityCodeForm, OfferForm, PriceForm, AvailabilityForm, ManufacturerCountryForm
from main.view.form_set import FormSet


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
        forms_clear = [OfferForm, WeightDimensionForm, ManufacturerCountryForm, UrlForm, BarcodeForm, ShelfLifeForm,
                       LifeTimeForm, GuaranteePeriodForm, CommodityCodeForm, AvailabilityForm]
        if self.offer:
            attrs = [offer, offer.weight_dimensions, offer.manufacturer_country, offer.url, offer.barcode,
                     offer.shelf_life, offer.life_time, offer.guarantee_period, offer.commodity_codes, offer]
        else:
            attrs = [None] * len(forms_clear)
        self.forms: list = self.cortege_from_lists(forms=forms_clear, attrs=attrs)

    def get_for_context(self) -> dict:
        forms: List[List] = [
            [list(self.forms_dict[OfferForm])[:6], *self.get_form_list([ManufacturerCountryForm,
                                                                        UrlForm, BarcodeForm, CommodityCodeForm])],
            self.get_form_list([ShelfLifeForm, LifeTimeForm, GuaranteePeriodForm]),
            self.get_form_list([WeightDimensionForm]), [list(self.forms_dict[OfferForm])[6:],
                                                        *self.get_form_list([AvailabilityForm])]
        ]
        accordions: list = ['Основная информация', 'Сроки', 'Габариты и вес в упаковке', 'Особенности логистики']
        return self.context(accordions=accordions, forms_context=forms)


class PriceFormSet(OfferBaseFormSet):
    def configure(self, offer=None):
        self.offer = offer
        self.forms: list = [(PriceForm, offer.get_price if offer else None),
                            (AvailabilityForm, offer if offer else None)]

    def get_for_context(self) -> dict:
        accordions: list = ['Управление ценой']
        forms: List[list] = [self.get_form_list([PriceForm])]
        return self.context(accordions=accordions, forms_context=forms)
