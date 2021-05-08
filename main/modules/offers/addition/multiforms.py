from typing import List
from main.forms import WeightDimensionForm, UrlForm, BarcodeForm, ShelfLifeForm, LifeTimeForm, \
    GuaranteePeriodForm, CommodityCodeForm, OfferForm, PriceForm, AvailabilityForm
from main.view import Multiform


class OfferMultiForm(Multiform):
    def __init__(self):
        self.offer = None

    def settings(self, offer=None):
        self.offer = offer
        self.forms: list = [(OfferForm, offer if offer else None), (WeightDimensionForm, offer.weight_dimensions if offer else None), (UrlForm, offer.url if offer else None),
                            (BarcodeForm, offer.barcode if offer else None), (ShelfLifeForm, offer.shelf_life if offer else None),
                            (LifeTimeForm, offer.life_time if offer else None),
                            (GuaranteePeriodForm, offer.guarantee_period if offer else None), (CommodityCodeForm, offer.commodity_codes if offer else None)]

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

    def write_foreign_key(self, instance):
        if hasattr(instance._meta.model, 'offer'):
            setattr(instance, 'offer', self.offer)
        return instance


class PriceMultiForm(Multiform):
    def __init__(self):
        self.offer = None

    def settings(self, offer=None):
        self.offer = offer
        self.forms: list = [(PriceForm, offer.get_price if offer else None), (AvailabilityForm, offer if offer else None)]

    def write_foreign_key(self, instance):
        if hasattr(instance._meta.model, 'offer'):
            setattr(instance, 'offer', self.offer)
        return instance

    def get_for_context(self) -> dict:
        accordions: list = ['Управление ценой', 'Управление поставками']
        forms: List[list] = [self.get_form_list([PriceForm]), self.get_form_list([AvailabilityForm])]
        return self.context(accordions=accordions, forms_context=forms)
