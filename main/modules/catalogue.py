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
            print(1)
            offer_list = OfferList()
            offer_list.save()
            offer_price = OfferPrice()
            offer_price.save()
            print('Update offer_db successful')
        search = request.GET.get('input', '').lower()
        fields = ['name', 'description', 'shopSku', 'category', 'vendor']
        objects = []
        for item in Offer.objects.all():
            try:
                for field in fields:
                    if search in getattr(item, field).lower():
                        objects.append(item)
            except:
                pass
        self.context['offers'] = objects
        return render(request, Page.catalogue, self.context)
