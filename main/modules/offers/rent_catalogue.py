from django.contrib import messages
from django.http import HttpResponse, HttpRequest

from main.forms.checkbox import CheckBoxSet
from main.models_addon.ya_market import Offer
from main.modules.base import BaseView
from main.view import get_navbar, Page, Filtration
from main.ya_requests import OfferList, OfferPrice

from django.shortcuts import render, redirect
from django.urls import reverse


class CatalogueRentView(BaseView):
    context = {'title': 'Rent_catalogue', 'page_name': 'Нерентабельные товары'}
    models_to_save = [OfferList, OfferPrice]
    fields = ['name', 'description', 'shopSku', 'category', 'vendor']
    table = ['', 'Название', 'SKU', 'Категория', 'Продавец']
    filtration = Filtration({
        "vendor": "Торговая марка",
        "category": "Категория",
        "availability": "Планы по поставкам",
    })

    def post(self, request: HttpRequest) -> HttpResponse:
        return self.save_models(request=request)

    def get(self, request: HttpRequest) -> HttpResponse:
        offers = [offer for offer in Offer.objects.filter(user=request.user) if offer.rent and offer.rent < 8]
        if not offers:
            messages.success(self.request, 'Все товары рентабельны')
            return redirect(reverse('catalogue_list'))
        filter_types = self.filtration.get_filter_types(offers)
        formset = CheckBoxSet(len(offers)).formset
        local_context = {
            'navbar': get_navbar(request),
            'table': self.table,
            'filter_types': filter_types.items(),
            'offers': [{'form': form, 'offer': offer} for form, offer in zip(formset, offers)]
        }
        self.context_update(local_context)
        return render(request, Page.catalogue, self.context)
