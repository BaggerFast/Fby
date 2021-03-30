from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from main.models import *
from main.modules.offers.product_card import Form
from main.view import *


class CreateOfferView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Create_offer', 'page_name': 'Создать товар'}

    def post(self, request):
        self.context['navbar'] = get_navbar(request)
        # request_post = request.POST.dict()
        # request_post['shopSku'] = offer.shopSku
        # request_post['marketSku'] = offer.marketSku
        offer = Offer.objects.create(user=request.user)
        form = Form()
        form.get_models_classes(key1={'id': offer.id}, key2={'offer': offer})
        form.get_post_form(disable=True, request=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар добавлен')
            self.context['disable'] = True
        else:
            form.get_post_form(disable=False, request=request.POST)
            offer.delete()
            self.context['disable'] = False
            self.context['create'] = True
        self.context['forms'] = form.get_form_for_context()
        return render(request, Page.product_card, self.context)

    def get(self, request):
        self.context['navbar'] = get_navbar(request)
        self.context['create'] = True
        form = Form()
        form.get_models_classes()
        form.get_clear_form(disable=False)
        self.context['forms'] = form.get_form_for_context()
        return render(request, Page.product_card, self.context)
