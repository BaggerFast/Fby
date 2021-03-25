from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from main.models import *
from main.forms import *
from main.view import *


class ProductPageView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Product_card', 'page_name': 'Карточка товара'}

    def get_models(self, id) -> dict:
        clear_model = [WeightDimension, Url, Barcode]

        models = {
            'offer': Offer.objects.get(id=id)
        }
        for model in clear_model:
            models.update({str(model()): model.objects.get(offer=models['offer'])})
            # timings = Timing.objects.get(offer=id)
        return models

    def get_form(self, disable, models: dict) -> dict:
        return {'Основная информация': ['offer_info', [OfferForm(instance=models["offer"], disable=disable),
                                                       UrlForm(instance=models['url'], disable=disable),
                                                       BarcodeForm(instance=models['barcode'], disable=disable)]],
                'Габариты и вес в упаковке': ['weight_info', [WeightDimensionForm(instance=models['weight'], disable=disable)]],
                'Особенности логистики': ['logistic_info', [LogisticForm(instance=models["offer"], disable=disable)]]}


    def get_form2(self, models:dict):
        return {'Основная информация': ['offer_info', [models['offer'],
                                                       models['url'],
                                                       models['barcode']]],
                'Габариты и вес в упаковке': ['weight_info',
                                              [models['weight']]],
                'Особенности логистики': ['logistic_info', models['logistic']]}

    def post(self, request, id):
        request_post = request.POST.dict()
        request_post['shopSku'] = current_offer.shopSku
        request_post['marketSku'] = current_offer.marketSku
        disable = True

        self.context['navbar'] = get_navbar(request)
        self.context['disable'] = disable

        models = self.get_models(id)
        models.update({'logistic': models['offer']})
        forms_list = [OfferForm, WeightDimensionForm, UrlForm, BarcodeForm, LogisticForm]
        forms_dict = {}
        for form in forms_list:
            forms_dict.update({str(form()): form})

        for key, value in models.items():
            forms_dict[key] = forms_dict[key](disable, request.POST, instance=value)
        valid = []
        for key, form in forms_dict.items():
            valid.append(form.is_valid())

        if not(False in valid):
            for key, form in forms_dict.items():
                form.save()
            self.context['forms'] = self.get_form2(forms_dict)
            messages.success(request, 'Данные успешно сохранены!')
        else:
            messages.error(request, 'Произошла ошибка!')
        return render(request, Page.product_card, self.context)

    def get(self, request, id):
        self.context['navbar'] = get_navbar(request)
        disable = False if int(request.GET.get('edit', 0)) else True
        self.context['disable'] = disable
        self.context['forms'] = self.get_form(disable=disable, models=self.get_models(id))
        return render(request, Page.product_card, self.context)
