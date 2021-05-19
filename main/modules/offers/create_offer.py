from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from main.models_addon.ya_market import Offer
from main.modules.offers.addition import OfferFormSet, PriceFormSet
from main.modules.base import BaseView
from main.view import get_navbar, Page


class CreateOfferView(BaseView):
    context = {'title': 'Create offer', 'page_name': 'Создать товар'}
    form = offer_id = None
    form_types = {"info": OfferFormSet, "accommodation": PriceFormSet}

    @staticmethod
    def convert_url(offer_id) -> HttpResponse:
        return redirect(reverse('create_offer') + f'?content=accommodation&id={offer_id}')

    def pre_init(self, request: HttpRequest):
        self.request: HttpRequest = request
        local_context = {
            'navbar': get_navbar(request),
            'content_disable': True,
            'content': request.GET.get('content', 'info')
        }
        self.context_update(local_context)
        if self.context['content'] in self.form_types:
            self.form = self.form_types[self.context['content']]()
            self.offer_id = int(request.GET.get('id', 0))
        else:
            raise Http404()

    def end_it(self):
        self.context_update({'id': self.offer_id, 'forms': self.form.get_for_context()})
        return render(self.request, Page.product_card, self.context)

    def save_message(self):
        if self.context['content'] == 'accommodation':
            messages.success(self.request, f'Товар добавлен. id = {self.offer_id}')
            return redirect(reverse('catalogue_offer'))
        else:
            messages.success(self.request, 'Первая часть модели сохранена')

    def post(self, request: HttpRequest) -> HttpResponse:
        self.pre_init(request=request)
        try:
            offer = Offer.objects.get(pk=self.offer_id)
        except ObjectDoesNotExist:
            offer = Offer.objects.create(user=self.request.user)
        self.form.configure(offer)
        self.form.set_post(post=request.POST)
        self.form.set_disable(True)
        if self.form.is_valid():
            self.form.save()
            message = self.save_message()
            if message:
                return message
        else:
            self.form.set_post(False)
            offer.delete()
            self.context['create'] = True
        if offer.id and self.context['content'] == 'info':
            return self.convert_url(offer.id)
        return self.end_it()

    def get(self, request: HttpRequest) -> HttpResponse:
        self.pre_init(request=request)
        self.context_update({'create': True, 'stage_next': self.context['content'] == 'info'})
        self.form.configure()
        self.form.set_empty()
        self.form.set_disable()
        if self.offer_id and self.context['content'] != 'accommodation':
            return self.convert_url(self.offer_id)
        return self.end_it()
