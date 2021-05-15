import operator
from functools import reduce

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.urls import reverse
from main.models_addon.ya_market import Offer
from main.modules.base import BaseView
from main.view import get_navbar, Page, Filtration
from main.ya_requests import OfferList, OfferPrice
import re


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
    types = [
        'Весь список',
        'Прошел модерацию',
        'На модерации',
        'Не прошел модерацию',
        'Не отправленные',
        'Не рентабельные',
        ]

    def find_offers_id_by_regular(self, request, regular_string=r'form-checkbox:'):
        offers_ids = [re.sub(regular_string, '', line) for line in list(dict(request.POST).keys())[1:-1]]
        return self.configure_offer(int(request.GET.get('content', 0))).filter(id__in=offers_ids)

    def post(self, request: HttpRequest) -> HttpResponse:
        if 'button_loader' in request.POST:
            return self.save_models(request=request)
        elif 'checkbox' in request.POST:
            for offer in self.find_offers_id_by_regular(request):
                offer.delete()
        return self.get(request)

    def configure_offer(self, index):
        query = {
            0: Q(),
            1: Q(processingState__status='READY'),
            2: Q(processingState__status='IN_WORK'),
            3: Q(processingState__status__in=['NEED_CONTENT', 'NEED_INFO', 'REJECTED', 'SUSPENDED', 'OTHER']),
            4: Q(processingState__isnull=True),
        }
        if index == 5:
            return [offer for offer in Offer.objects.filter(user=self.request.user) if offer.check_rent]
        return Offer.objects.filter(user=self.request.user).filter(query[index])

    def get(self, request: HttpRequest) -> HttpResponse:
        self.request = request
        category_index = int(request.GET.get('content', 0))
        offers = self.configure_offer(category_index)
        if not offers and category_index:
            messages.error(self.request, f'Каталог {self.types[category_index].lower()} пуст')
            return redirect(reverse('catalogue_list'))
        filter_types = self.filtration.get_filter_types(offers)
        local_context = {
            'navbar': get_navbar(request),
            'table': self.table,
            'filter_types': filter_types.items(),
            'current_type': category_index,
            'types': self.types,
            'offers': self.sort_object(offers, filter_types),
        }
        self.context_update(local_context)
        return render(request, Page.catalogue, self.context)
