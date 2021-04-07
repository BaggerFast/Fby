from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from main.forms.offer import *
from main.models import Offer, Price
from main.view import Page, get_navbar, Multiform
from main.yandex.request import OfferChangePrice


class Form(Multiform):
    def set_forms(self, key1: dict = None, key2: dict = None) -> None:
        forms: list = [WeightDimensionForm, UrlForm, BarcodeForm, WeightDimensionForm, ShelfLifeForm, LifeTimeForm,
                       GuaranteePeriodForm, CommodityCodeForm]
        self.forms_model_list: list[dict] = \
            [{'attrs': key1, 'form': OfferForm}] + [{'attrs': key2, 'form': form} for form in forms]

    def get_for_context(self) -> dict:
        forms: list[list] = [
            [list(self.forms_dict[str(OfferForm())].form)[:6],
             *self.get_form_list([UrlForm, BarcodeForm, CommodityCodeForm])],
            self.get_form_list([ShelfLifeForm, LifeTimeForm, GuaranteePeriodForm]),
            self.get_form_list([WeightDimensionForm]),
            [list(self.forms_dict[str(OfferForm())].form)[6::]]
        ]
        accordions: list = ['Основная информация', 'Сроки', 'Габариты и вес в упаковке', 'Особенности логистики']
        return self.context(forms=forms, accordions=accordions)


class PriceF(Multiform):
    def set_forms(self, key1: dict = None, key2: dict = None) -> None:
        forms: list = [PriceForm]
        self.forms_model_list: list[dict] = \
            [{'attrs': key1, 'form': AvailabilityForm}] + [{'attrs': key2, 'form': form} for form in forms]

    def get_for_context(self) -> dict:
        accordions: list = ['Управление ценой', 'Управление поставками']
        forms: list[list] = [self.get_form_list([PriceForm]), self.get_form_list([AvailabilityForm])]
        return self.context(forms=forms, accordions=accordions)


class ProductPageView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Product_card', 'page_name': 'Карточка товара'}
    form = None
    request = None

    def pre_init(self, pk, request):
        self.request = request
        self.context['navbar'] = get_navbar(request)
        self.context['content'] = request.GET.get('content', 'info')
        correct_content = ['info', 'accommodation']
        if self.context['content'] in correct_content:
            self.form = Form() if self.context['content'] == 'info' else PriceF() \
                if self.context['content'] == 'accommodation' else None
            self.form.set_forms(key1={'id': pk}, key2={'offer': Offer.objects.get(id=pk)})
        else:
            raise Http404()

    def end_it(self, disable) -> HttpResponse:
        self.context['forms'] = self.form.get_for_context()
        self.context['disable'] = disable
        return render(self.request, Page.product_card, self.context)

    def post(self, request, pk) -> HttpResponse:
        self.pre_init(pk=pk, request=request)
        self.form.set_post(disable=True, request=request.POST)
        if self.form.is_valid():
            self.form.save()
            messages.success(request, 'Редактирование прошло успешно!')
            # todo save on button
            # OfferChangePrice(price_list=list(Price.objects.filter(offer_id=pk)))
            disable = True
        else:
            disable = False
            self.form.set_post(disable=False, request=request.POST)
        return self.end_it(disable=disable)

    def get(self, request, pk) -> HttpResponse:
        self.pre_init(pk=pk, request=request)
        disable = False if int(request.GET.get('edit', 0)) else True
        self.form.set_fill(disable=disable)
        return self.end_it(disable=disable)
