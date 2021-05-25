from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, Http404
from django.urls import reverse
from main.models_addon.ya_market import Offer
from main.modules.base import BaseView
from main.view import get_navbar, Page, Filtration
from main.ya_requests import OfferList, OfferPrice, UpdateOfferList, YandexChangePricesList
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
    content_types = {
        'Весь список': Q(),
        'Прошли модерацию': Q(processingState__status='READY'),
        'На модерации': Q(processingState__status='IN_WORK'),
        'Не прошли модерацию': Q(processingState__status__in=['NEED_CONTENT', 'NEED_INFO', 'REJECTED', 'SUSPENDED',
                                                              'OTHER']),
        'Изменены локально': Q(processingState__isnull=False) & (Q(has_changed=True) | Q(price__has_changed=True)),
        'Созданы локально': Q(),
        'Не рентабельные': None,
    }

    def find_offers_id_by_regular(self, request, regular_string=r'form-checkbox:'):
        """Метод для получения товаров, отмеченных в checkbox"""
        offers_ids = [re.sub(regular_string, '', line) for line in list(dict(request.POST).keys())[1:-1]]
        return self.configure_offer().filter(id__in=offers_ids)

    def update_price(self, offers):
        """"Обработка запроса на изменение цены на Яндексе"""
        prices = [offer.get_price for offer in offers if offer.price.has_changed]

        if not prices:
            return
        sku_list = offers.values_list('shopSku', flat=True).distinct()
        changed_prices = YandexChangePricesList(prices=prices, request=self.request)
        changed_prices.update_prices()
        changed_prices.messages(sku_list=sku_list, success_message="Все цены успешно отправлены")

    def save_to_ym(self, offers):
        """Обработка запроса на обновление или сохранение товара на Яндексе"""
        offers = offers.filter(has_changed=True)
        if not offers:
            return
        sku_list = offers.values_list('shopSku', flat=True).distinct()
        update_request = UpdateOfferList(offers=list(offers), request=self.request)
        update_request.update_offers()
        update_request.messages(sku_list=sku_list, success_message="Все товары успешно отправлены")

    def button_push(self):
        offers = self.find_offers_id_by_regular(self.request)
        if not offers:
            offers = self.configure_offer()
        self.save_to_ym(offers=offers)
        self.update_price(offers=offers)
        return redirect(reverse('catalogue_offer'))

    def check_box(self):
        [offer.delete() for offer in self.find_offers_id_by_regular(self.request)]
        return redirect(reverse('catalogue_offer'))

    def post(self, request: HttpRequest) -> HttpResponse:
        self.request = request
        data = {
            'button_loader': lambda: self.save_models(request=request, name='catalogue_offer'),
            'button_push': self.button_push,
            'checkbox': self.check_box,
        }
        for key in data.keys():
            if key in request.POST:
                return data[key]()
        return redirect(reverse('catalogue_offer'))

    def configure_offer(self):
        index = self.request.GET.get('content', 'Весь список')
        """Метод для получения товаров с нужным статусом"""
        if index not in self.content_types:
            raise Http404()
        if index == 'Не рентабельные':
            return [offer for offer in Offer.objects.filter(user=self.request.user).select_related('price')
                    if offer.check_rent]
        return Offer.objects.filter(Q(user=self.request.user) & self.content_types[index])

    def get(self, request: HttpRequest) -> HttpResponse:
        self.request = request
        category_index = request.GET.get('content', 'Весь список')
        if category_index not in self.content_types:
            raise Http404()
        offers = self.configure_offer()
        if not offers and category_index != 'Весь список':
            messages.success(self.request, f'Каталог {category_index.lower()} пуст')
            return redirect(reverse('catalogue_offer'))
        filter_types = self.filtration.get_filter_types(offers)
        local_context = {
            'navbar': get_navbar(request),
            'table': self.table,
            'filter_types': filter_types.items(),
            'current_type': category_index,
            'types': self.content_types,
            'offers': self.sort_object(offers, filter_types),
        }
        self.context_update(local_context)
        return render(request, Page.catalogue, self.context)
