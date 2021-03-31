from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from main.models import *
from main.modules.offers.product_card import Form, TempForm
from main.view import *


class CreateOfferView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Create_offer', 'page_name': 'Создать товар'}

    def preinit(self, request):
        self.context['navbar'] = get_navbar(request)
        self.context['content'] = request.GET.get('content', 'info')
        self.form = Form() if self.context['content'] == 'info' else TempForm() \
            if self.context['content'] == 'accommodation' else None
        self.form.get_models_classes()

    def endit(self):
        self.context['forms'] = self.form.get_for_context()

    def post(self, request):
        self.preinit(request=request)
        offer = Offer.objects.create(user=request.user)
        form = Form()
        form.get_models_classes(key1={'id': offer.id}, key2={'offer': offer})
        form.get_post(disable=True, request=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар добавлен')
            self.context['disable'] = True
        else:
            form.get_post(disable=False, request=request.POST)
            offer.delete()
            self.context['disable'] = False
            self.context['create'] = True
        self.context['forms'] = form.get_for_context()
        return render(request, Page.product_card, self.context)

    def get(self, request):
        self.preinit(request=request)
        self.context['create'] = True
        self.form.get_models_classes()
        self.form.get_clear(disable=False)
        self.endit()
        return render(request, Page.product_card, self.context)
