from django.shortcuts import render
from django.views.generic.base import View
from main.request_yandex import OfferList, OfferChangePrice
from main.views import Page, get_navbar
from main.models.base import Offer


class CatalogueView(View):
    context = {}

    def get(self, request):
        self.context['navbar'] = get_navbar(request)
        if int(request.GET.get('update_data', 0)):
            data = OfferList()
            data.save()
            # OfferChangePrice({'656593390': {'price': 1000}})
            print('Update offer_db successful')
        self.context['offers'] = Offer.objects.all()
        return render(request, Page.catalogue, self.context)
