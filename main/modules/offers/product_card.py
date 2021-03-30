from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View

from main.forms.offer import CommodityCodeForm
from main.models import *
from main.forms import *
from main.view import *


class Form(Multiform):
    def get_models_classes(self, key1: dict = None, key2: dict = None) -> None:
        self.model_list = [{'attrs': key1, 'form': OfferForm}]
        forms = [WeightDimensionForm, UrlForm, BarcodeForm,  WeightDimensionForm, ShelfLifeForm, LifeTimeForm,
                 GuaranteePeriodForm, CommodityCodeForm]
        for form in forms:
            self.model_list.append({'attrs': key2, 'form': form})

    def get_form_for_context(self) -> dict:
        return {'Основная информация': ['offer_info', [list(self.models_json[str(OfferForm())].form)[:6],
                                                       self.models_json[str(UrlForm())].form,
                                                       self.models_json[str(BarcodeForm())].form,
                                        self.models_json[str(CommodityCodeForm())].form]],
                'Сроки': ['timing_info', [self.models_json[str(ShelfLifeForm())].form,
                                          self.models_json[str(LifeTimeForm())].form,
                                          self.models_json[str(GuaranteePeriodForm())].form]],
                'Габариты и вес в упаковке': ['weight_info', [self.models_json[str(WeightDimensionForm())].form]],
                'Особенности логистики': ['logistic_info', [list(self.models_json[str(OfferForm())].form)[6::]]]}


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
            messages.success(request, 'Редактирование прошло успешно!')
            self.context['disable'] = True
        else:
            self.context['disable'] = False
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
