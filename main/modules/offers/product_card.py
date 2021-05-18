"""Модуль для отображения карточки товара"""
import math

from django.contrib import messages
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect

from main.forms import AvailabilityForm, PriceForm
from main.models_addon.ya_market import Offer, Price
from main.modules.offers.addition import OfferFormSet, PriceFormSet
from main.modules.base import BaseView
from main.view import Page, get_navbar
from main.ya_requests.price import ChangePrices, YandexChangePricesList
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

    def offer_has_changed(self):
        """Возвращает True, если было изменено хотя бы одно поле Товара"""
        if self.context['content'] == 'info':
            return self.form.has_changed()
        else:
            return self.form.forms_dict[AvailabilityForm].has_changed()

    def prise_has_changed(self):
        """Возвращает True, если было изменено хотя бы одно поле Цены"""
        if self.context['content'] == 'accommodation':
            return self.form.forms_dict[PriceForm].has_changed()
        else:
            return False

    def end_it(self, pk) -> HttpResponse:
        """Окончательная настройка контекста и отправка ответа на запрос"""
        offers = Offer.objects.get(pk=pk)
        rent = offers.check_rent
        if rent:
            messages.error(self.request, f'Рентабельность: {offers.rent} % < 8%. Не прибыльно!!!')
        self.context_update({'forms': self.form.get_for_context(),
                             'disable': self.disable,
                             'offer': Offer.objects.get(pk=pk)})
        return render(self.request, Page.product_card, self.context)

    def save_to_ym(self, offer):
        """Обработка запроса на обновление или сохранение товара на Яндексе"""
        if offer.has_changed:
            sku = offer.shopSku
            update_request = UpdateOfferList(offers=[offer], request=self.request)
            update_request.update_offers()
            if sku not in update_request.errors:
                messages.success(self.request, f'Товар shopSku = {sku} успешно сохранен на Яндексе')
                return
            errors = f'Ошибка при сохранении товара shopSku = {sku} на Яндексе.'
            errors += ''.join(update_request.errors[sku])
            messages.error(self.request, errors)

    def update_price(self, offer):
        """"Обработка запроса на изменение цены на Яндексе"""
        if offer.get_price and offer.get_price.has_changed:
            price = [offer.get_price]
            sku = offer.shopSku
            changed_prices = YandexChangePricesList(prices=list(price), request=self.request)
            changed_prices.update_prices()
            if not sku in changed_prices.errors:
                messages.success(self.request, f'Цена товара shopSku = {sku} успешно сохранена на Яндексе')
                return
            errors = f'Ошибка при сохранении цены товара shopSku = {sku} на Яндексе. '
            errors += ' '.join(changed_prices[sku])
            messages.error(self.request, errors)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Обработка post-запроса"""

        def delete() -> HttpResponse:
            """Обработка запроса на удаление товара с перенаправлением на страницу каталога."""
            offer = get_object_or_404(Offer, id=pk)
            offer.delete()
            messages.success(request, f'Товар "{offer.name}" успешно удален')
            return redirect(reverse('catalogue_offer'))

        self.request = request
        self.pk = pk

        if 'delete' in request.POST:
            return delete()

        btns = {
            'offer': self.save_to_ym,
            'price': self.update_price
        }

        data = request.POST.get('yandex', '')
        if data in btns:
            offer = Offer.objects.select_related('price').get(pk=pk)
            btns[data](offer)
            return self.get(request, pk)

        self.pre_init(request=request, pk=pk)
        self.form.set_post(post=self.request.POST)
        self.form.set_disable(True)
        self.disable = self.form.is_valid()
        if self.disable:
            self.form.save()
            if self.offer_has_changed():
                Offer.objects.filter(id=pk).update(has_changed=True)
            if self.prise_has_changed():
                Price.objects.filter(offer_id=pk).update(has_changed=True)
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
