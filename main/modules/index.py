from django.contrib import messages
from django.shortcuts import render
from django.views.generic.base import View
from main.view import Navbar, Page


class MainView(View):
    """отображение главной страницы"""
    context = {'title': 'Главная'}

    def post(self, request):
        messages.success(request, 'Информация отправлена')
        self.context['navbar'] = Navbar(request).get()
        return render(request, Page.index, self.context)

    def get(self, request):
        self.context['navbar'] = Navbar(request).get()
        return render(request, Page.index, self.context)
