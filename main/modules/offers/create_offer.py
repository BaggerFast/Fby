from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from main.models import Offer, Price
from main.modules.offers.product_card import Form, TempForm
from main.view import get_navbar, Page


def convert_url(offer_id) -> HttpResponse:
    return redirect(reverse('create_offer') + '?content=accommodation&id=' + str(offer_id))


class CreateOfferView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Create_offer', 'page_name': 'Создать товар'}
    form = None
    offer_id = None

    def pre_init(self, request):
        self.context['navbar'] = get_navbar(request)
        self.context['content_disable'] = True
        self.context['content'] = request.GET.get('content', 'info')
        if self.context['content'] in ['info', 'accommodation']:
            self.form = Form() if self.context['content'] == 'info' else TempForm() \
                if self.context['content'] == 'accommodation' else None
            self.offer_id = int(request.GET.get('id', -1))
        else:
            raise Http404()

    def end_it(self):
        self.context['id'] = self.offer_id
        self.context['forms'] = self.form.get_for_context()

    def save_message(self, request):
        data = None
        if self.context['content'] == 'accommodation':
            messages.success(request, f'Товар добавлен. id = {self.offer_id}')
            data = redirect(reverse('catalogue_list'))
        else:
            messages.success(request, 'Первая часть модели сохранена')
        return data

    def post(self, request) -> HttpResponse:
        self.pre_init(request=request)
        if self.offer_id < 0:
            offer = Offer.objects.create(user=request.user)
            self.offer_id = offer.id
        else:
            offer = Offer.objects.get(pk=self.offer_id)
        self.form.get_models_classes(key1={'id': self.offer_id}, key2={'offer': offer})
        self.form.get_post(disable=True, request=request.POST)
        if self.form.is_valid():
            self.form.save()
            message = self.save_message(request)
            if message:
                return message
        else:
            print('da')
            self.form.get_post(disable=False, request=request.POST)
            offer.delete()
            self.context['create'] = True
        self.end_it()
        if self.offer_id >= 0 and self.context['content'] == 'info':
            return convert_url(offer_id=self.offer_id)
        return render(request, Page.product_card, self.context)

    def get(self, request) -> HttpResponse:
        self.pre_init(request=request)
        self.context['create'] = True
        self.context['stage_next'] = True if self.context['content'] == 'info' else False
        self.form.get_models_classes()
        self.form.get_clear(disable=False)
        self.end_it()
        if self.offer_id >= 0 and self.context['content'] != 'accommodation':
            return convert_url(offer_id=self.offer_id)
        return render(request, Page.product_card, self.context)
