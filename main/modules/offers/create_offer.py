from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from main.models import Offer
from main.modules.offers import OfferMultiForm, PriceMultiForm
from main.modules.base import BaseView
from main.view import get_navbar, Page


def convert_url(offer_id) -> HttpResponse:
    return redirect(reverse('create_offer') + '?content=accommodation&id=' + str(offer_id))


class CreateOfferView(BaseView):
    context = {'title': 'Create offer', 'page_name': 'Создать товар'}
    form = None
    offer_id = None
    form_types = {"info": OfferMultiForm, "accommodation": PriceMultiForm}

    def pre_init(self, request):
        self.request = request
        local_context = {'navbar': get_navbar(request),
                         'content_disable': True,
                         'content': request.GET.get('content', 'info')}
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
            return redirect(reverse('catalogue_list'))
        else:
            messages.success(self.request, 'Первая часть модели сохранена')

    def post(self, request) -> HttpResponse:
        self.pre_init(request=request)
        if not self.offer_id:
            offer = Offer.objects.create(user=request.user)
            self.offer_id = offer.id
        else:
            offer = Offer.objects.get(pk=self.offer_id)
        self.form.set_forms(self.offer_id)
        self.form.set_post(disable=True, post=request.POST)
        if self.form.is_valid():
            self.form.save()
            message = self.save_message()
            if message:
                return message
        else:
            self.form.set_post(disable=False, post=request.POST)
            offer.delete()
            self.context['create'] = True
        if self.offer_id and self.context['content'] == 'info':
            return convert_url(self.offer_id)
        return self.end_it()

    def get(self, request) -> HttpResponse:
        self.pre_init(request=request)
        self.context_update({'create': True, 'stage_next': self.context['content'] == 'info'})
        self.form.set_forms()
        self.form.set_clear(disable=False)
        if self.offer_id and self.context['content'] != 'accommodation':
            return convert_url(self.offer_id)
        return self.end_it()
