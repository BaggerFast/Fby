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
            errors = OfferList().save() if OfferList().save() else None
            OfferPrice().save()
            print('Update offer_db successful')
        self.context['offers'] = self.offer_search(request, self.del_sku_from_name(Offer.objects.all()))
        return render(request, Page.catalogue, self.context)

    def del_sku_from_name(self, offers_list) -> list:
        offers = offers_list
        data = ['upper', 'lower']
        for i in range(len(offers)):
            if offers[i].shopSku.lower() in offers[i].name.lower():
                for dat in data:
                    sku = getattr(offers[i].shopSku, dat)()
                    offers[i].name = offers[i].name.replace(sku, '')
        return offers

    def offer_search(self, request, offers) -> list:
        search = request.GET.get('input', '').lower()
        self.context['search'] = True if len(search) else False
        fields = ['name', 'description', 'shopSku', 'category', 'vendor']
        objects = []
        for item in offers:
            try:
                for field in fields:
                    if search in getattr(item, field).lower():
                        objects.append(item)
            except:
                pass
        return objects
