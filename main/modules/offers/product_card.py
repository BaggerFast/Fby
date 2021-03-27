from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from main.models import *
from main.forms import *
from main.view import *


class FormParser:
    def __init__(self, attrs_for_filter: dict, model, form, disabled: bool, request=False):
        self.request = request
        try:
            self.model = model.objects.filter(**attrs_for_filter)[0]
        except IndexError:
            model.objects.create(**attrs_for_filter).save()
            self.model = model.objects.filter(**attrs_for_filter)[0]
        self.form_base = form
        self.post(disabled) if request else self.get(disabled)

    def get(self, disabled):
        self.form = self.form_base(instance=self.model, disable=disabled)

    def post(self, disabled):
        self.form = self.form_base(disabled, self.request, instance=self.model)


class Form:
    def __init__(self, offer, request=None):
        self.offer = offer
        self.request = request
        self.model_list = self.get_models_classes()

    def get_models_classes(self):
        key = {'offer': self.offer}
        return [(Offer, {'id': self.offer.id}, OfferForm), (WeightDimension, key, WeightDimensionForm),
                (Url, key, UrlForm), (Barcode, key, BarcodeForm), (Offer, {'id': self.offer.id}, LogisticForm),
                (ShelfLife, key, ShelfLifeForm), (LifeTime, key, LifeTimeForm),
                (GuaranteePeriod, key, GuaranteePeriodForm)]

    def post_get_form(self, disable):
        self.models_json = {}
        for model in self.model_list:
            self.models_json.update(
                {str(model[2]()): FormParser(attrs_for_filter=model[1], model=model[0], form=model[2],
                                             disabled=disable, request=self.request)})

    def get_form(self, disable):
        self.models_json = {}
        for model in self.model_list:
            self.models_json.update(
                {str(model[2]()): FormParser(attrs_for_filter=model[1], model=model[0], form=model[2],
                                             disabled=disable)})

    def get_form_for_context(self):
        return {'Основная информация': ['offer_info', [self.models_json[str(OfferForm())].form,
                                                       self.models_json[str(UrlForm())].form,
                                                       self.models_json[str(BarcodeForm())].form]],
                'Сроки': ['timing_info', [self.models_json[str(ShelfLifeForm())].form,
                                          self.models_json[str(LifeTimeForm())].form,
                                          self.models_json[str(GuaranteePeriodForm())].form]],
                'Габариты и вес в упаковке': ['weight_info', [self.models_json[str(WeightDimensionForm())].form]],
                'Особенности логистики': ['logistic_info', [self.models_json[str(LogisticForm())].form]]}

    def is_valid(self):
        for key, model in self.models_json.items():
            if not model.form.is_valid():
                return False
        return True

    def save(self):
        for key, model in self.models_json.items():
            model.form.save()


class ProductPageView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Product_card', 'page_name': 'Карточка товара'}

    def post(self, request, id):
        self.context['navbar'] = get_navbar(request)
        offer = Offer.objects.get(id=id)

        # request_post = request.POST.dict()
        # request_post['shopSku'] = offer.shopSku
        # request_post['marketSku'] = offer.marketSku

        form = Form(offer=offer, request=request.POST)
        form.post_get_form(disable=True)
        if form.is_valid():
            form.save()
            messages.success(request, 'Все успешно')
            self.context['disable'] = True
        else:
            form.get_form(disable=False)
            self.context['disable'] = False
            messages.error(request, 'Произошла ошибка!')
        self.context['forms'] = form.get_form_for_context()
        return render(request, Page.product_card, self.context)

    def get(self, request, id):
        self.context['navbar'] = get_navbar(request)
        disable = False if int(request.GET.get('edit', 0)) else True
        offer = Offer.objects.get(id=id)
        form = Form(offer=offer)
        form.get_form(disable=disable)
        self.context['disable'] = disable
        self.context['forms'] = form.get_form_for_context()
        print(self.context['forms'])

        return render(request, Page.product_card, self.context)
