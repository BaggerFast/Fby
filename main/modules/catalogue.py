from django.shortcuts import render
from django.views.generic.base import View
from main.models.ya_market.base import Offer
from main.request_yandex import OfferList, OfferPrice
from main.views import Page, get_navbar


class CatalogueView(View):
    """отображение каталога"""
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}

    def get(self, request):
        self.context['navbar'] = get_navbar(request)
        if int(request.GET.get('update_data', 0)):
            OfferList().save()
            OfferPrice().save()
            print('Update offer_db successful')
        self.context['offers'] = self.del_sku_from_name(Offer.objects.all())

        return render(request, Page.catalogue, self.context)

    def del_sku_from_name(self, offers_list):
        offers = offers_list
        for i in range(len(offers)):
            if offers[i].shopSku.lower() in offers[i].name.lower():
                sku = offers[i].shopSku.upper()
                offers[i].name = offers[i].name.replace(sku, '')

                sku = offers[i].shopSku.lower()
                offers[i].name = offers[i].name.replace(sku, '')
        return offers
