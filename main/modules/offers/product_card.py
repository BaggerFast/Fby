from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from main.models_addon import Offer, Price
from main.modules.offers import OfferMultiForm, PriceMultiForm
from main.modules.base import BaseView
from main.view import Page, get_navbar
from main.ya_requests.price import ChangePrices


class ProductPageView(BaseView):
    context = {'title': 'Product card', 'page_name': 'Карточка товара'}
    form = None
    disable: bool = False
    form_types = {"info": OfferMultiForm, "accommodation": PriceMultiForm}

    def pre_init(self, pk, request):
        self.context_update({'navbar': get_navbar(request), 'content': request.GET.get('content', 'info')})
        if self.context['content'] in self.form_types:
            self.form = self.form_types[self.context['content']]()
            self.form.set_forms(pk=pk)
        else:
            raise Http404()

    def end_it(self) -> HttpResponse:
        self.context_update({'forms': self.form.get_for_context(), 'disable': self.disable})
        return render(self.request, Page.product_card, self.context)

    def post(self, request, pk) -> HttpResponse:

        def delete() -> HttpResponse:
            offer = Offer.objects.get(id=pk)
            messages.success(request, f'Товар "{offer.name}" успешно удален')
            offer.delete()
            return redirect(reverse('catalogue_list'))

        # todo добавить price в функцию
        def update_price(price):
            ChangePrices(['ya_requests', 'update'], price_list=[price], request=request)
            if price != Price.objects.get(offer_id=pk):
                messages.error(request, 'Данные о товаре не изменились')

        if 'delete' in request.POST:
            return delete()

        # есть лямбда функции не забывайте
        # ошибки: message.error('текст ошибки') прописать в своих классах сохранения
        buttons = {
            'offer': None,  # todo (offer) вставить функцию для сохранения текущего оффера + вывести ошибки
            'price': update_price
        }

        btn = request.POST.get('yandex', '')

        if btn in buttons.keys():
            pass
            # buttons[btn]()

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
        self.pre_init(request=request, pk=pk)
        self.disable = not bool(self.request.GET.get('edit', 0))
        self.form.set_fill(disable=self.disable)
        return self.end_it()
