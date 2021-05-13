from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.urls import reverse

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
    types = [
            'Весь список',
            'Прошел модерацию',
            'На модерации',
            'Не прошел модерацию',
            'Не рентабельные',
            ]

    def post(self, request: HttpRequest) -> HttpResponse:
        if 'button_loader' in request.POST:
            return self.save_models(request=request)
        elif 'checkbox' in request.POST:
            numbers = [int(box.split('-')[1]) for box in list(dict(request.POST).keys())[1:-1]]
            offers = self.configure_offer(int(request.GET.get('content', 0)))
            filter_types = self.filtration.get_filter_types(offers)
            sorted_obj = self.sort_object(offers, filter_types)
            for number in numbers:
                sorted_obj[number].delete()
        return self.get(request)

    def configure_offer(self, index):
        offers = Offer.objects.filter(user=self.request.user)
        types = {
            0: lambda: offers,
            1: lambda: [offer for offer in offers if offer.processingState.status == 'READY'],
            2: lambda: [offer for offer in offers if offer.processingState.status == 'IN_WORK'],
            3: lambda: [offer for offer in offers if offer.processingState.status in ['NEED_INFO', 'REJECTED',
                                                                                        'SUSPENDED', 'OTHER']],
            4: lambda: [offer for offer in offers if offer.rent and offer.rent < 8],
        }
        return types[index]()

    def get(self, request: HttpRequest) -> HttpResponse:
        self.request = request
        category_index = int(request.GET.get('content', 0))
        offers = self.configure_offer(category_index)
        if not offers:
            messages.error(self.request, f'Каталог {self.types[category_index].lower()} пуст')
            return redirect(reverse('catalogue_list'))
        filter_types = self.filtration.get_filter_types(offers)
        sorted_obj = self.sort_object(offers, filter_types)
        formset = CheckBoxSet(len(sorted_obj)).formset
        local_context = {
            'navbar': get_navbar(request),
            'table': self.table,
            'filter_types': filter_types.items(),
            'formset': formset,
            'current_type': category_index,
            'types': self.types,
            'offers': [{'form': form, 'offer': offer} for form, offer in zip(formset, sorted_obj)]
        }
        self.context_update(local_context)
        return render(request, Page.catalogue, self.context)
