from pprint import pprint
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render
from main.modules.offers import OfferMultiForm, PriceMultiForm
from main.modules.offers.base_offer_view import BaseOfferView
from main.view import Page, get_navbar


class ProductPageView(BaseOfferView):
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
        self.pre_init(request=request, pk=pk)
        pprint(request.POST)
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
