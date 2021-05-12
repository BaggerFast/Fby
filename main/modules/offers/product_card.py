"""Модуль для отображения карточки товара"""
import math

from django.contrib import messages
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from main.models_addon.ya_market import Offer, Price
from main.modules.offers.addition import OfferFormSet, PriceFormSet
from main.modules.base import BaseView
from main.view import Page, get_navbar
from main.ya_requests.price import ChangePrices
from main.ya_requests.request import UpdateOfferList


class ProductPageView(BaseView):
    """
    Класс, управляющий отображением карточки товара
    """
    context = {'title': 'Product card', 'page_name': 'Карточка товара'}
    form = None
    disable: bool = False
    form_types = {"info": OfferFormSet, "accommodation": PriceFormSet}

    def pre_init(self, pk: int, request: HttpRequest) -> None:
        """Предварительная настройка контекста"""
        self.context_update({'navbar': get_navbar(request),
                             'content': request.GET.get('content', 'info')})
        if self.context['content'] in self.form_types:
            self.form = self.form_types[self.context['content']]()
            self.form.configure(offer=Offer.objects.get(pk=pk))
        else:
            raise Http404()

    def end_it(self, pk) -> HttpResponse:
        """Окончательная настройка контекста и отправка ответа на запрос"""
        rent = Offer.objects.get(pk=pk).rent
        if rent:
            self.context['rent'] = math.floor(rent)
            if rent < 8:
                messages.error(self.request, f'Рентабельность: {math.floor(rent)}% < 8%. Не прибыльно!!!')
        self.context_update({'forms': self.form.get_for_context(), 'disable': self.disable})
        return render(self.request, Page.product_card, self.context)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Обработка post-запроса"""

        def delete() -> HttpResponse:
            """Обработка запроса на удаление товара с перенаправлением на страницу каталога."""
            offer = get_object_or_404(Offer, id=pk)
            offer.delete()
            messages.success(request, f'Товар "{offer.name}" успешно удален')
            return redirect(reverse('catalogue_list'))

        def update_price() -> HttpResponse:
            """"Обработка запроса на изменение цены на Яндексе"""
            price = Price.objects.get(offer_id=pk)
            ChangePrices(['ya_requests', 'update'], price_list=[price], request=request)
            return redirect(reverse('catalogue_list'))

        def save_to_ym() -> HttpResponse:
            """Обработка запроса на обновление или сохранение товара на Яндексе"""
            offer = Offer.objects.get(id=pk)
            sku = offer.shopSku
            update_request = UpdateOfferList(offers=[offer], request=request)
            update_request.update_offers()

            if sku in update_request.success:
                messages.success(request, f'Товар shopSku = {sku} успешно сохранен на Яндексе')
            elif sku in update_request.errors:
                messages.error(request, f'Ошибка при сохранении товара shopSku = {sku} на Яндексе.')
                for error_text in update_request.errors[sku]:
                    messages.error(request, error_text)
            return self.get(request, pk)

        if 'delete' in request.POST:
            return delete()

        buttons = {
            'offer': save_to_ym,
            'price': update_price
        }

        btn = request.POST.get('yandex', '')
        if btn in buttons.keys():
            return buttons[btn]()

        self.pre_init(request=request, pk=pk)
        self.form.set_post(post=self.request.POST)
        self.form.set_disable(True)
        self.disable = self.form.is_valid()
        if self.disable:
            self.form.save()
        else:
            self.form.set_disable(False)
        return self.end_it(pk)

    def get(self, request: HttpRequest, pk) -> HttpResponse:
        """Обработка get-запроса"""
        self.pre_init(request=request, pk=pk)
        self.disable = not bool(self.request.GET.get('edit', 0))
        self.form.set_fill()
        self.form.set_disable(self.disable)
        return self.end_it(pk)
