from django.shortcuts import render
from django.views.generic.base import View
from main.models.ya_market.base import Offer
from main.request_yandex import OfferList
from main.views import Page, get_navbar


class CatalogueView(View):
    """отображение каталога"""
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}

    def get(self, request):
        self.context['navbar'] = get_navbar(request)
        if int(request.GET.get('update_data', 0)):
            data = OfferList()
            data.save()
            print('Update offer_db successful')
        self.context['offers'] = Offer.objects.all()
        return render(request, Page.catalogue, self.context)
