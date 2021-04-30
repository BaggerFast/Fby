from django.shortcuts import render
from django.http import HttpResponse
from main.models_addon import Offer
from main.modules.base import BaseView
from main.view import get_navbar, Page
from main.ya_requests import OfferList, OfferPrice


class CatalogueView(BaseView):
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}
    models_to_save = [OfferList, OfferPrice]

    def reformat_offer(self, offer) -> list:
        def offer_search(offers) -> list:
            def search_algorithm():
                if not len(keywords):
                    return offers
                scores = {}
                for item in offers:
                    for keyword in keywords:
                        for field in fields:
                            attr = getattr(item, field)
                            if attr is not None and keyword in str(attr).lower():
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

        return offer_search(offer)

    def post(self, request) -> HttpResponse:
        return self.save_models(request=request)

    def get(self, request) -> HttpResponse:
        local_context = {
            'navbar': get_navbar(request),
            'offers': self.reformat_offer(offer=Offer.objects.filter(user=request.user)),
            'table': ["Название", "SKU", "Категория", "Продавец", "Картинка"]
        }
        self.context_update(local_context)

        return render(request, Page.catalogue, self.context)
