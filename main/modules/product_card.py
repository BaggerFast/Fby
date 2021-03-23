from django.shortcuts import render
from django.views.generic.base import View

from main.forms.from_db import OfferForm, WeightDimensionForm, LogisticForm, UrlForm, BarcodeForm, TimingForm
from main.models.ya_market.base import Offer
from main.models.ya_market.support import WeightDimension, Url, Barcode, Timing
from main.views import Page, get_navbar


class ProductPageView(View):
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

        self.context['logistic_form'] = LogisticForm(instance=offer, disable=disable)
        self.context['url_form'] = UrlForm(instance=url, disable=disable)
        self.context['barcode_form'] = BarcodeForm(instance=barcode, disable=disable)
        # self.context['timing_form'] = TimingForm(instance=timings)
        self.context['offer_form'] = OfferForm(instance=offer, disable=disable)
        self.context['weight_form'] = WeightDimensionForm(instance=weight, disable=disable)

        return render(request, Page.product_card, self.context)
