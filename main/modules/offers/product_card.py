"""Модуль для отображения карточки товара"""

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from main.models_addon import Offer
from main.modules.offers import OfferMultiForm, PriceMultiForm
from main.modules.base import BaseView
from main.view import Page, get_navbar
from main.ya_requests.request import UpdateOfferList


class ProductPageView(BaseView):
    """
    Класс, управляющий отображением карточки товара
    """
    context = {'title': 'Product card', 'page_name': 'Карточка товара'}
    form = None
    disable: bool = False
    form_types = {"info": OfferMultiForm, "accommodation": PriceMultiForm}

    def pre_init(self, pk: int, request) -> None:
        """Предварительная настройка контекста"""
        self.context_update({'navbar': get_navbar(request),
                             'content': request.GET.get('content', 'info')}
                            )
        if self.context['content'] in self.form_types:
            self.form = self.form_types[self.context['content']]()
            self.form.set_forms(pk=pk)
        else:
            raise Http404()

    def end_it(self) -> HttpResponse:
        """Окончательная настройка контекста и отправка ответа на запрос"""
        self.context_update({'forms': self.form.get_for_context(), 'disable': self.disable})
        return render(self.request, Page.product_card, self.context)

    def post(self, request, pk: int) -> HttpResponse:
        """Обработка post-запроса"""

        def delete() -> HttpResponse:
            """Обработка запроса на удаление товара с перенаправлением на страницу каталога."""
            offer = Offer.objects.get(id=pk)
            offer.delete()
            messages.success(request, f'Товар "{offer.name}" успешно удален')
            return redirect(reverse('catalogue_list'))

        def save_to_ym() -> None:
            """Обработка запроса на обновление или сохранение товара на Яндексе"""
            offer = Offer.objects.get(id=pk)
            sku = offer.shopSku
            update_request = UpdateOfferList([offer])
            update_request.update_offers()

            if sku in update_request.success:
                success_message = f'Товар shopSku = {sku} успешно сохранен на Яндексе'
                messages.success(request, success_message)
            elif sku in update_request.errors:
                error_message = f'Ошибка при сохранении товара shopSku = {sku} на Яндексе.'
                messages.error(request, error_message)
                for error_text in update_request.errors[sku]:
                    messages.error(request, error_text)

        if 'delete' in request.POST:
            return delete()

        # есть лямбда функции не забывайте
        # ошибки: message.error('текст ошибки') прописать в своих классах сохранения
        buttons = {
            'offer': save_to_ym,
            'price': None,  # todo (price) вставить функцию для сохранения текущей цены(если цена не поменялась
                            # и вывести ошибку
        }

        btn = request.POST.get('yandex', '')

        if btn in buttons.keys():
            buttons[btn]()
            self.get(request, pk)

        self.pre_init(request=request, pk=pk)
        self.form.set_post(disable=True, post=self.request.POST)
        if self.form.is_valid():
            self.form.save()
            self.disable = True
        else:
            self.disable = False
            self.form.set_post(disable=self.disable, post=self.request.POST)
        return self.end_it()

    def get(self, request, pk) -> HttpResponse:
        """Обработка get-запроса"""
        self.pre_init(request=request, pk=pk)
        self.disable = not bool(self.request.GET.get('edit', 0))
        self.form.set_fill(disable=self.disable)
        return self.end_it()
