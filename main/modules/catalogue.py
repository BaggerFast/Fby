from django.shortcuts import render, redirect
from django.views.generic.base import View
from main.models.ya_market.base import Offer
from main.request_yandex import OfferList, OfferPrice
from main.views import Page, get_navbar


class CatalogueView(View):
    """отображение каталога"""
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}

    def get(self, request):
        if request.user.is_authenticated:
            self.context['navbar'] = get_navbar(request)
            if int(request.GET.get('update_data', 0)):
                OfferList(request.user).save()
                OfferPrice(request.user).save()
                print('Update offer_db successful')
                objects = self.offer_search(request)
            self.context['offers'] = self.del_sku_from_name(Offer.objects.filter(user=request.user))

            return render(request, Page.catalogue, self.context)
        else:
            return redirect('index')

    def del_sku_from_name(self, offers_list):
        offers = offers_list
        for i in range(len(offers)):
            if offers[i].shopSku.lower() in offers[i].name.lower():
                sku = offers[i].shopSku.upper()
                offers[i].name = offers[i].name.replace(sku, '')

                sku = offers[i].shopSku.lower()
                offers[i].name = offers[i].name.replace(sku, '')
        return offers

    def offer_search(self, request) -> list:
        search = request.GET.get('input', '').lower()
        self.context['search'] = True if len(search) else False
        fields = ['name', 'description', 'shopSku', 'category', 'vendor']
        objects = []
        for item in Offer.objects.all():
            try:
                for field in fields:
                    if search in getattr(item, field).lower():
                        objects.append(item)
            except:
                pass
        return objects
