from django.shortcuts import render
from django.http import HttpResponse
from main.models import Offer, Url
from main.modules.offers.base_offer_view import BaseOfferView
from main.view import get_navbar, Page
from main.yandex import OfferList, OfferPrice


class CatalogueView(BaseOfferView):
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}
    models_to_save = [OfferList, OfferPrice]

    def post(self, request) -> HttpResponse:
        for model in self.models_to_save:
            if not model().save(request=request):
                break
        return self.get(request=request)

    def get(self, request) -> HttpResponse:
        offer = Offer.objects.filter(user=request.user)
        local_context = {
            'navbar': get_navbar(request),
            'count': offer.count(),
            'offers': self.reformat_offer(offer),
            'urls': Url.objects.filter(offer=offer),
            'table': ["Название", "SKU", "Категория", "Продавец", "Картинка"]
        }
        self.context_update(local_context)

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

        def search_algorithm():
            if not len(keywords):
                return offers
            scores = {}
            for item in offers:
                for keyword in keywords:
                    for field in fields:
                        attr = getattr(item, field)
                        if attr is not None and keyword in attr.lower():
                            if item not in scores:
                                scores[item] = 0
                            scores[item] += 1
                            break
            return sorted(scores, key=scores.get, reverse=True)

        search = self.request.GET.get('input', '').lower()
        fields = ['name', 'description', 'shopSku', 'category', 'vendor']
        keywords = search.strip().split()
        objects = search_algorithm()
        self.context_update({'search': bool(len(search)), 'count': len(objects)})
        return objects
