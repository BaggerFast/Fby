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
                    return objects
                scores = {}
                for item in objects:
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

        return offer_search(append_images())

    def post(self, request) -> HttpResponse:
        for model in self.models_to_save:
            if not model().save(request=request):
                break
        return self.get(request=request)

    def get(self, request) -> HttpResponse:
        offer = Offer.objects.filter(user=request.user)
        filter_types = self.filtration.get_filter_types(offer)
        local_context = {
            'navbar': get_navbar(request),
            'count': offer.count(),
            'offers': self.reformat_offer(offer, filter_types),
            'urls': Url.objects.filter(),
            'table': self.table,
            'filter_types': filter_types.items(),
        }
        self.context_update(local_context)
        return render(request, Page.catalogue, self.context)
