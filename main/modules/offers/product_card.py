from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from main.models import *
from main.forms import *
from main.view import *


class ProductPageView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Product_card', 'page_name': 'Карточка товара'}

    def get(self, request, id):
        self.context['navbar'] = get_navbar(request)

        offer = Offer.objects.get(id=id)
        weight = WeightDimension.objects.get(offer=id)
        url = Url.objects.get(offer=id)
        barcode = Barcode.objects.get(offer=id)
        # timings = Timing.objects.get(offer=id)

        disable = False if int(request.GET.get('edit', 0)) else True

        self.context['disable'] = disable
        self.context['forms'] = {'Основная информация': ['offer_info', [OfferForm(instance=offer, disable=disable),
                                                         UrlForm(instance=url, disable=disable),
                                                         BarcodeForm(instance=barcode, disable=disable)]],
                                'Габариты и вес в упаковке': ['weight_info', [WeightDimensionForm(instance=weight, disable=disable)]],
                                'Особенности логистики': ['logistic_info', [LogisticForm(instance=offer, disable=disable)]]}
        # self.context['timing_form'] = TimingForm(instance=timings)

        return render(request, Page.product_card, self.context)
