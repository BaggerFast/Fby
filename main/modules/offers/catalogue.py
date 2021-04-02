from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from main.models import *
from main.view import *
from main.yandex import *
from main.yandex.request_yandex import OfferChangePrice


class CatalogueView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}
    models_to_save = [OfferList, OfferPrice]

    def get(self, request):
        self.request = request
        self.context['navbar'] = get_navbar(request)
        if int(request.GET.get('update_data', 0)):
            for model in self.models_to_save:
                if not model().save_with_message(request=request):
                    break
        offer = Offer.objects.filter(user=request.user)

        self.context['count'] = offer.count()
        self.context['offers'] = self.reformat_offer(offer)
        self.context['urls'] = Url.objects.filter(offer=offer)

        return render(request, Page.catalogue, self.context)

    def reformat_offer(self, offer) -> list:
        return self.offer_search(CatalogueView.append_images(offer))

    @staticmethod
    def append_images(offers_list) -> list:
        offers = offers_list
        for i in range(len(offers)):
            try:
                setattr(offers[i], 'image', Url.objects.filter(offer=offers[i])[0].url)
            except IndexError:
                pass
        return offers

    def offer_search(self, offers) -> list:
        search = self.request.GET.get('input', '').lower()
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
        self.context['count'] = len(objects)
        return objects
