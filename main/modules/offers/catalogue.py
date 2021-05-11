from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from main.models_addon import Offer
from main.modules.base import BaseView
from main.view import get_navbar, Page, Filtration
from main.ya_requests import OfferList, OfferPrice


class CatalogueView(BaseView):
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}
    models_to_save = [OfferList, OfferPrice]
    fields = ['name', 'description', 'shopSku', 'category', 'vendor']
    table = ['Название', 'SKU', 'Категория', 'Продавец']
    filtration = Filtration({
        "vendor": "Торговая марка",
        "category": "Категория",
        "availability": "Планы по поставкам",
    })

    def post(self, request: HttpRequest) -> HttpResponse:
        return self.save_models(request=request)

    def get(self, request: HttpRequest) -> HttpResponse:
        offers = Offer.objects.filter(user=request.user)
        filter_types = self.filtration.get_filter_types(offers)
        local_context = {
            'navbar': get_navbar(request),
            'offers': self.sort_object(offers, filter_types),
            'table': self.table,
            'filter_types': filter_types.items(),
        }
        self.context_update(local_context)
        return render(request, Page.catalogue, self.context)
