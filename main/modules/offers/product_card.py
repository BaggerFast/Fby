from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from main.models import *
from main.forms import *
from main.view.views import Multiform
from main.view import *


class Form(Multiform):
    def get_models_classes(self, key1: dict = None, key2: dict = None) -> None:
        self.model_list = [(Offer, key1, OfferForm), (WeightDimension, key2, WeightDimensionForm),
                           (Url, key2, UrlForm), (Barcode, key2, BarcodeForm),
                           (ShelfLife, key2, ShelfLifeForm), (LifeTime, key2, LifeTimeForm),
                           (GuaranteePeriod, key2, GuaranteePeriodForm)]

    def get_form_for_context(self) -> dict:
        return {'Основная информация': ['offer_info', [list(self.models_json[str(OfferForm())].form)[:6],
                                                       self.models_json[str(UrlForm())].form,
                                                       self.models_json[str(BarcodeForm())].form]],
                'Сроки': ['timing_info', [self.models_json[str(ShelfLifeForm())].form,
                                          self.models_json[str(LifeTimeForm())].form,
                                          self.models_json[str(GuaranteePeriodForm())].form]],
                'Габариты и вес в упаковке': ['weight_info', [self.models_json[str(WeightDimensionForm())].form]],
                'Особенности логистики': ['logistic_info', [list(self.models_json[str(OfferForm())].form)[7::]]]}


class ProductPageView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Product_card', 'page_name': 'Карточка товара'}

    def post(self, request, id):
        self.context['navbar'] = get_navbar(request)
        # request_post = request.POST.dict()
        # request_post['shopSku'] = offer.shopSku
        # request_post['marketSku'] = offer.marketSku

        form = Form()
        form.get_models_classes(key1={'id': id}, key2={'offer': Offer.objects.get(id=id)})
        form.get_post_form(disable=True, request=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменено')
            self.context['disable'] = True
        else:
            form.get_fill_form(disable=False)
            self.context['disable'] = False
            messages.error(request, 'Произошла ошибка!')
        self.context['forms'] = form.get_form_for_context()
        return render(request, Page.product_card, self.context)

    def get(self, request, id):
        self.context['navbar'] = get_navbar(request)
        disable = False if int(request.GET.get('edit', 0)) else True
        form = Form()
        form.get_models_classes(key1={'id': id}, key2={'offer': Offer.objects.get(id=id)})
        form.get_fill_form(disable=disable)

        self.context['disable'] = disable
        self.context['forms'] = form.get_form_for_context()

        return render(request, Page.product_card, self.context)
