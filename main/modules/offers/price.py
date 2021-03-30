from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from main.models import *
from main.view import *
from main.forms import *


class Form(Multiform):
    def get_models_classes(self, key1: dict = None, key2: dict = None) -> None:
        self.model_list = [{'attrs': key1, 'form': AvailabilityForm}]
        forms = [PriceForm]
        for form in forms:
            self.model_list.append({'attrs': key2, 'form': form})

    def get_form_for_context(self) -> dict:
        return {'Цена': ['offer_price', [self.models_json[str(PriceForm())].form]],
                'Размещение': ['offer_availability', [self.models_json[str(AvailabilityForm())].form]]}


class CreateOfferView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Price', 'page_name': 'Управление размещением'}

    # def post(self, request, id):
    #     # self.context['navbar'] = get_navbar(request)
    #     # offer = Offer.objects.create(user=request.user)
    #     # form = Form()
    #     # form.get_models_classes(key1={'id': offer.id}, key2={'offer': offer})
    #     # form.get_post_form(disable=True, request=request.POST)
    #     # if form.is_valid():
    #     #     form.save()
    #     #     messages.success(request, 'Товар добавлен')
    #     #     self.context['disable'] = True
    #     # else:
    #     #     form.get_post_form(disable=False, request=request.POST)
    #     #     offer.delete()
    #     #     self.context['disable'] = False
    #     #     self.context['create'] = True
    #     # self.context['forms'] = form.get_form_for_context()
    #     # return render(request, Page.product_card, self.context)

    def get(self, request, id):
        self.context['navbar'] = get_navbar(request)
        self.context['create'] = False
        form = Form()
        form.get_models_classes(key1={'id': id}, key2={'offer': Offer.objects.get(id=id)})
        form.get_fill_form(disable=False)
        self.context['forms'] = form.get_form_for_context()
        return render(request, Page.product_card, self.context)
