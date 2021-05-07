from typing import List
from main.forms import WeightDimensionForm, UrlForm, BarcodeForm, ShelfLifeForm, LifeTimeForm, \
    GuaranteePeriodForm, CommodityCodeForm, OfferForm, PriceForm, AvailabilityForm
from main.view import Multiform


class OfferMultiForm(Multiform):
    def __init__(self, offer):
        super().__init__()
        self.offer = offer
        self.forms: list = [(OfferForm, offer), (WeightDimensionForm, offer.weight_dimensions), (UrlForm, offer.url),
                            (BarcodeForm, offer.barcode), (ShelfLifeForm, offer.shelf_life),
                            (LifeTimeForm, offer.life_time),
                            (GuaranteePeriodForm, offer.guarantee_period), (CommodityCodeForm, offer.commodity_codes)]

    def get_fill_form(self):
        for attrs in self.forms:
            self.forms_dict.update({attrs[0]: attrs[0](instance=attrs[1])})

        for form in self.forms_dict.values():
            form.turn_off()

    def set_disable(self, disable):
        for form in self.forms_dict.values():
            form.turn_off(disable)

    def set_post(self, post):
        for attrs in self.forms:
            self.forms_dict.update({attrs[0]: attrs[0](post, instance=attrs[1])})

        for form in self.forms_dict.values():
            form.turn_off()

    def get_for_context(self) -> dict:
        forms: List[List] = [
            [
                list(self.forms_dict[OfferForm])[:6],
                *self.get_form_list([UrlForm, BarcodeForm, CommodityCodeForm])
            ],
            self.get_form_list([ShelfLifeForm, LifeTimeForm, GuaranteePeriodForm]),
            self.get_form_list([WeightDimensionForm]),
            [
                list(self.forms_dict[OfferForm])[6:]
            ]
        ]
        accordions: list = ['Основная информация', 'Сроки', 'Габариты и вес в упаковке', 'Особенности логистики']
        return self.context(accordions=accordions, forms_context=forms)

    def is_valid(self) -> bool:
        for form in self.forms_dict.values():
            if not form.is_valid():
                return False
        return True

    def save(self):
        for form in self.forms_dict.values():
            form.save()


class PriceMultiForm(Multiform):
    def set_forms(self, pk=None) -> None:
        self.forms_model_list: List[dict] = [{'attrs': {'offer_id': pk}, 'form': PriceForm},
                                             {'attrs': {'id': pk}, 'form': AvailabilityForm}]

    def get_for_context(self) -> dict:
        accordions: list = ['Управление ценой', 'Управление поставками']
        forms: List[list] = [self.get_form_list([PriceForm]), self.get_form_list([AvailabilityForm])]
        return self.context(forms=forms, accordions=accordions)
