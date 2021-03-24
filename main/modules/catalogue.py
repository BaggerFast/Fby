from django.contrib import messages
from django.shortcuts import render
from django.views.generic.base import View
from main.models.ya_market.base import Offer
from main.models.ya_market.support import Url
from main.request_yandex import OfferList, OfferPrice
from main.views import Page, get_navbar


class CatalogueView(View):
    """отображение каталога"""
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}
    models_to_save = [OfferList, OfferPrice]

    def get(self, request):
        self.context['navbar'] = get_navbar(request)
        if int(request.GET.get('update_data', 0)):
            for model in self.models_to_save:
                flag = model().save_with_message(request=request)
                if not flag:
                    break
        offer = Offer.objects.filter(user=request.user)
        self.context['offers'] = self.offer_search(request, self.append_images(self.del_sku_from_name(offer)))
        self.context['urls'] = Url.objects.filter(offer=offer)
        return render(request, Page.catalogue, self.context)

    def append_images(self, offers_list) -> list:
        offers = offers_list
        for i in range(len(offers)):
            try:
                setattr(offers[i], 'image', Url.objects.filter(offer=offers[i])[0])
            except IndexError:
                pass
        return offers

    def del_sku_from_name(self, offers_list) -> list:
        offers = offers_list
        data = ['upper', 'lower']
        for i in range(len(offers)):
            if str(offers[i].shopSku).lower() in str(offers[i].name).lower():
                for dat in data:
                    sku = getattr(str(offers[i].shopSku), dat)()
                    offers[i].name = str(offers[i].name).replace(sku, '')
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
                        break
            except:
                pass
        return objects
