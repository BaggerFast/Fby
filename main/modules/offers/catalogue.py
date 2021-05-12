from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from main.forms.checkbox import CheckBoxSet
from main.models_addon.ya_market import Offer
from main.modules.base import BaseView
from main.view import get_navbar, Page, Filtration
from main.ya_requests import OfferList, OfferPrice


class CatalogueView(BaseView):
    context = {'title': 'Catalogue', 'page_name': 'Каталог'}
    models_to_save = [OfferList, OfferPrice]
    fields = ['name', 'description', 'shopSku', 'category', 'vendor']
    table = ['', 'Название', 'SKU', 'Категория', 'Продавец']
    filtration = Filtration({
        "vendor": "Торговая марка",
        "category": "Категория",
        "availability": "Планы по поставкам",
    })

    def post(self, request: HttpRequest) -> HttpResponse:
        if 'button_loader' in request.POST:
            return self.save_models(request=request)
        elif 'checkbox' in request.POST:
            numbers = [int(box.split('-')[1]) for box in list(dict(request.POST).keys())[1:-1]]
            offers = Offer.objects.filter(user=request.user)
            filter_types = self.filtration.get_filter_types(offers)
            sorted_obj = self.sort_object(offers, filter_types)
            for number in numbers:
                sorted_obj[number].delete()
        return self.get(request)

    def get(self, request: HttpRequest) -> HttpResponse:
        offers = Offer.objects.filter(user=request.user)
        filter_types = self.filtration.get_filter_types(offers)
        sorted_obj = self.sort_object(offers, filter_types)
        formset = CheckBoxSet(len(sorted_obj)).formset
        local_context = {
            'navbar': get_navbar(request),
            'offers': sorted_obj,
            'table': self.table,
            'filter_types': filter_types.items(),
            'formset': formset,
            'table_lines': [{'form': form, 'offer': offer} for form, offer in zip(formset, sorted_obj)]
        }
        self.context_update(local_context)
        return render(request, Page.catalogue, self.context)
