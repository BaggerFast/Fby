from django.shortcuts import render
from django.http import HttpResponse
from main.models import Offer, Url
from main.modules.offers.base_offer_view import BaseOfferView
from main.view import get_navbar, Page
from main.yandex import OfferList, OfferPrice


class CatalogueView(BaseOfferView):
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}
    models_to_save = [OfferList, OfferPrice]
    table = ["Название", "Описание", "SKU", "Категория", "Продавец", "Картинка"]
    fields_to_filter = {"category": 3, "vendor": 4}

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
            'table': self.table,
            'filter_types': self.get_filter_types(offer).items(),
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

    def get_filter_types(self, offers):
        # PLACEHOLDER START
        filter_types = {}
        for field, table_index in self.fields_to_filter.items():
            filter_types[field] = {
                'name': self.table[table_index],
                'options': ['Фильтры', 'Лампы для автомобилей', 'Масляные фильтры', 'VOLKSWAGEN']
            }
        return filter_types
        # PLACEHOLDER END

    def filters_from_request(self):
        filters = {}
        for field, _ in self.fields_to_filter.items():
            filters[field] = self.request.GET.get(field)
        return filters

    @staticmethod
    def filter_offers(offers, filters):
        scores = []
        for offer in offers:
            for filter_name, filter_param in filters.items():
                if filter_param:
                    offer_param = getattr(offer, filter_name)
                    if offer_param == filter_param:
                        if offer not in scores:
                            scores.append(offer)
                else:
                    scores.append(offer)
        for offer in scores:
            for filter_name, filter_param in filters.items():
                if filter_param or filter_param != '':
                    offer_param = getattr(offer, filter_name)
                    if offer_param != filter_param:
                        scores.remove(offer)
        return scores

    def offer_search(self, offers) -> list:

        def search_algorithm():
            if len(keywords) == 0:
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
        filters = self.filters_from_request()
        objects = self.filter_offers(offers, filters)
        objects = search_algorithm()
        self.context_update({'search': bool(len(search)), 'count': len(objects)})
        return objects
