from django.shortcuts import render
from django.views.generic.base import View

from main.forms.from_db import OfferForm, WeightDimensionForm, LogisticForm
from main.models.ya_market.base import Offer
from main.models.ya_market.support import WeightDimension
from main.views import Page, get_navbar


class ProductPageView(View):
    """отображение каталога"""
    context = {'title': 'Product_card', 'page_name': 'Карточка товара'}

    def get(self, request, id):
        self.context['navbar'] = get_navbar(request)
        offer = Offer.objects.get(id=id)
        weight = WeightDimension.objects.get(offer=id)

        self.context['logistic_form'] = LogisticForm(instance=offer)
        self.context['offer_form'] = OfferForm(instance=offer)
        self.context['weight_form'] = WeightDimensionForm(instance=weight)

        return render(request, Page.product_card, self.context)
