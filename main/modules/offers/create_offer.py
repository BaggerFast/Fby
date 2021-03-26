from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from main.models import *
from main.forms import *
from main.view import *


class CreateOfferView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Create_offer', 'page_name': 'Создать товар'}

    def get_form(self, disable) -> dict:
        return {'Основная информация': ['offer_info', [OfferForm(instance=Offer(), disable=disable),
                                                       UrlForm(instance=Url(), disable=disable),
                                                       BarcodeForm(instance=Barcode(), disable=disable)]],
                'Габариты и вес в упаковке': ['weight_info', [WeightDimensionForm(instance=WeightDimension(), disable=disable)]],
                'Особенности логистики': ['logistic_info', [LogisticForm(instance=Offer(), disable=disable)]]}

    def get(self, request):
        self.context['navbar'] = get_navbar(request)
        disable = False if int(request.GET.get('edit', 0)) else True
        self.context['create'] = True
        self.context['forms'] = self.get_form(disable=False)
        return render(request, Page.product_card, self.context)
