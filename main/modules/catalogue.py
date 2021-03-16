from django.shortcuts import render
from django.views.generic.base import View
from main.RequestYd import OfferList
from main.views import *


class CatalogueView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {
            'offers': None
        }

    def get(self, request):
        data = OfferList()
        data.saver()
        self.context['offers'] = Offer.objects.all()
        return render(request, Page.catalogue, self.context)
