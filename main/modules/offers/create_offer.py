from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from main.models import *
from main.modules.offers.product_card import Form, TempForm
from main.view import *


class CreateOfferView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Create_offer', 'page_name': 'Создать товар'}

    def pre_init(self, request):
        self.context['navbar'] = get_navbar(request)
        self.context['content'] = request.GET.get('content', 'info')
        correct_content = ['info', 'accommodation']
        if self.context['content'] in correct_content:
            self.form = Form() if self.context['content'] == 'info' else TempForm() \
                if self.context['content'] == 'accommodation' else None
            self.form.get_models_classes()
        else:
            raise Http404()

    def end_it(self):
        self.context['forms'] = self.form.get_for_context()

    def post(self, request):
        self.pre_init(request=request)
        id = int(request.GET.get('id', -1))
        if id < 0:
            offer = Offer.objects.create(user=request.user)
            id = offer.id
            self.context['id'] = id
        else:
            offer = Offer.objects.get(id=id)
        self.form.get_post(disable=True, request=request.POST)
        self.form.get_models_classes(key1={'id': offer.id}, key2={'offer': offer})
        if self.form.is_valid():
            print('VALID')
            messages.success(request, 'Товар добавлен')
            self.context['disable'] = True
            self.form.save()
        else:
            self.form.get_post(disable=False, request=request.POST)
            offer.delete()
            self.context['disable'] = False
            self.context['create'] = True
        self.context['forms'] = self.form.get_for_context()

        if id >= 0 and self.context['content'] == 'info':
            return redirect(reverse('create_offer')+'?content=accommodation&id='+str(id))

        return render(request, Page.product_card, self.context)

    def get(self, request):
        self.pre_init(request=request)
        self.context['create'] = True
        self.form.get_models_classes()
        self.form.get_clear(disable=False)
        self.end_it()
        if int(request.GET.get('id', -1)) >= 0 and self.context['content'] != 'accommodation':
            return redirect(reverse('create_offer')+'?content=accommodation&id='+str(request.GET.get('id', -1)))
        return render(request, Page.product_card, self.context)
