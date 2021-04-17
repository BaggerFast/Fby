from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from main.models_addon import Offer
from main.modules.offers import OfferMultiForm, PriceMultiForm
from main.modules.base import BaseView
from main.view import Page, get_navbar


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

        if 'delete' in request.POST:
            return delete()

        self.pre_init(request=request, pk=pk)
        self.form.set_post(disable=True, post=self.request.POST)
        if self.form.is_valid():
            self.form.save()
            messages.success(self.request, 'Редактирование прошло успешно!')
            # todo save on button
            # YandexChangePrices(price_list=list(Price.objects.filter(offer_id=pk)))
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
