from typing import List

from main.forms.offer import WeightDimensionForm, UrlForm, BarcodeForm, ShelfLifeForm, LifeTimeForm, \
    GuaranteePeriodForm, CommodityCodeForm, OfferForm, PriceForm, AvailabilityForm
from main.view import Multiform


class OfferMultiForm(Multiform):
    def set_forms(self, pk=None) -> None:
        forms: list = [WeightDimensionForm, UrlForm, BarcodeForm, ShelfLifeForm, LifeTimeForm,
                       GuaranteePeriodForm, CommodityCodeForm]
        self.forms_model_list: List[dict] = \
            [{'attrs': {'id': pk}, 'form': OfferForm}] + [{'attrs': {'offer_id': pk}, 'form': form} for form in forms]

    def get_for_context(self) -> dict:
        forms: List[List] = [
            [
                list(self.forms_dict[str(OfferForm())].form)[:6],
                *self.get_form_list([UrlForm, BarcodeForm, CommodityCodeForm])
            ],
            self.get_form_list([ShelfLifeForm, LifeTimeForm, GuaranteePeriodForm]),
            self.get_form_list([WeightDimensionForm]),
            [
                list(self.forms_dict[str(OfferForm())].form)[6:]
            ]
        ]
        accordions: list = ['Основная информация', 'Сроки', 'Габариты и вес в упаковке', 'Особенности логистики']
        return self.context(forms=forms, accordions=accordions)


class PriceMultiForm(Multiform):
    def set_forms(self, pk=None) -> None:
        self.forms_model_list: List[dict] = [{'attrs': {'offer_id': pk}, 'form': PriceForm},
                                             {'attrs': {'id': pk}, 'form': AvailabilityForm}]

    def get_for_context(self) -> dict:
        accordions: list = ['Управление ценой', 'Управление поставками']
        forms: List[list] = [self.get_form_list([PriceForm]), self.get_form_list([AvailabilityForm])]
        return self.context(forms=forms, accordions=accordions)
