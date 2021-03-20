from django.shortcuts import render
from django.views.generic.base import View
from main.request_yandex import OfferList
from main.views import Page
from main.models.base import Offer


class CatalogueView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {
            'offers': None
        }

    def get(self, request):
        # data = OfferList()
        # data.save()
        self.context['offers'] = Offer.objects.all()
        return render(request, Page.catalogue, self.context)
