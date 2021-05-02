from django.shortcuts import render
from django.http import HttpResponse
from main.models_addon import Offer, Url
from main.modules.base import BaseView
from main.view import get_navbar, Page, Filtration
from main.ya_requests import OfferList, OfferPrice


class CatalogueView(BaseView):
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}
    models_to_save = [OfferList, OfferPrice]
    table = ["Название", "SKU", "Категория", "Продавец", "Картинка"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filtration = Filtration({
            "vendor": "Торговая марка",
            "category": "Категория",
            "availability": "Планы по поставкам",
        })

    def reformat_offer(self, offer, filter_types) -> list:
        def offer_search(offers) -> list:
            def search_algorithm():
                if not len(keywords):
                    return objects
                scores = {}
                for item in objects:
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
            filters = self.filtration.filters_from_request(self.request, filter_types)
            objects = self.filtration.filter_items(offers, filters)
            objects = search_algorithm()
            was_searching_used = len(search) != 0
            for filter_value in filters.values():
                if filter_value and len(filter_value) != 0:
                    was_searching_used = True
                    break
            self.context_update({'search': was_searching_used, 'count': len(objects)})
            return objects
        return offer_search(offer)

    def post(self, request) -> HttpResponse:
        return self.save_models(request=request)

    def get(self, request) -> HttpResponse:
        offers = Offer.objects.filter(user=request.user)
        filter_types = self.filtration.get_filter_types(offers)
        local_context = {
            'navbar': get_navbar(request),
            'offers': self.reformat_offer(offers, filter_types),
            'table': self.table,
            'filter_types': filter_types.items(),
        }
        self.context_update(local_context)
        return render(request, Page.catalogue, self.context)
