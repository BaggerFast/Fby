from django.shortcuts import render
from django.http import HttpResponse
from main.models_addon import Offer, Url
from main.modules.base import BaseView
from main.view import get_navbar, Page
from main.ya_requests import OfferList, OfferPrice


class CatalogueView(BaseView):
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}
    models_to_save = [OfferList, OfferPrice]

    def reformat_offer(self, offer) -> list:
        def append_images() -> list:
            offers = offer
            for i in range(len(offers)):
                try:
                    setattr(offers[i], 'image', Url.objects.filter(offer=offers[i])[0].url)
                except IndexError:
                    pass
            return offers

        def offer_search(offers) -> list:
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

        return offer_search(append_images())

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
            'offers': self.reformat_offer(offer=offer),
            'urls': Url.objects.filter(),
            'table': ["Название", "SKU", "Категория", "Продавец", "Картинка"]
        }
        self.context_update(local_context)

        return render(request, Page.catalogue, self.context)

