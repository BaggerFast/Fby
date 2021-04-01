from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View
from main.forms.offer import *
from main.models import Offer
from main.view import Page, get_navbar, Multiform


class Form(Multiform):
    def get_models_classes(self, key1: dict = None, key2: dict = None) -> None:
        self.model_list = [{'attrs': key1, 'form': OfferForm}]
        forms = [WeightDimensionForm, UrlForm, BarcodeForm, WeightDimensionForm, ShelfLifeForm,
                 LifeTimeForm, GuaranteePeriodForm, CommodityCodeForm]
        for form in forms:
            self.model_list.append({'attrs': key2, 'form': form})

    def get_for_context(self) -> dict:
        return {'Основная информация': ['offer_info',
                                        [list(self.models_json[str(OfferForm())].form)[:6],
                                         self.models_json[str(UrlForm())].form,
                                         self.models_json[str(BarcodeForm())].form,
                                         self.models_json[str(CommodityCodeForm())].form]],
                'Сроки': ['timing_info',
                          [self.models_json[str(ShelfLifeForm())].form,
                           self.models_json[str(LifeTimeForm())].form,
                           self.models_json[str(GuaranteePeriodForm())].form]],
                'Габариты и вес в упаковке': ['weight_info',
                                              [self.models_json[str(WeightDimensionForm())].form]],
                'Особенности логистики': ['logistic_info',
                                          [list(self.models_json[str(OfferForm())].form)[6::]]]}


class TempForm(Multiform):
    def get_models_classes(self, key1: dict = None, key2: dict = None) -> None:
        self.model_list = [{'attrs': key1, 'form': AvailabilityForm}]
        forms = [PriceForm]
        for form in forms:
            self.model_list.append({'attrs': key2, 'form': form})

    def get_for_context(self) -> dict:
        return {'Управление ценой': ['price_edit',
                                     [self.models_json[str(PriceForm())].form]],
                'Управление поставками': ['deliveries_edit',
                                          [self.models_json[str(AvailabilityForm())].form]]}


class ProductPageView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Product_card', 'page_name': 'Карточка товара'}
    form = None

    def pre_init(self, id, request):
        self.context['navbar'] = get_navbar(request)
        self.context['content'] = request.GET.get('content', 'info')
        correct_content = ['info', 'accommodation']
        if self.context['content'] in correct_content:
            self.form = Form() if self.context['content'] == 'info' else TempForm() \
                if self.context['content'] == 'accommodation' else None
            self.form.get_models_classes(key1={'id': id}, key2={'offer': Offer.objects.get(id=id)})
        else:
            raise Http404()

    def end_it(self, disable):
        self.context['forms'] = self.form.get_for_context()
        self.context['disable'] = disable

    def post(self, request, id):
        # request_post = request.POST.dict()
        # request_post['shopSku'] = offer.shopSku
        # request_post['marketSku'] = offer.marketSku
        self.pre_init(id=id, request=request)
        self.form.get_post(disable=True, request=request.POST)
        if self.form.is_valid():
            self.form.save()
            messages.success(request, 'Редактирование прошло успешно!')
            disable = True
        else:
            disable = False
            self.form.get_post(disable=False, request=request.POST)
        self.end_it(disable=disable)
        return render(request, Page.product_card, self.context)

    def get(self, request, id):
        self.pre_init(id=id, request=request)
        disable = False if int(request.GET.get('edit', 0)) else True
        self.form.get_fill(disable=disable)
        self.end_it(disable=disable)
        return render(request, Page.product_card, self.context)
