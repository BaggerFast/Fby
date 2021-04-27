from django.shortcuts import render
from django.views.generic.base import View
from main.view import *


class MainView(View):
    """отображение главной страницы"""
    context = {'title': 'Main'}

    def get(self, request):
        self.context['navbar'] = get_navbar(request)
        return render(request, Page.index, self.context)
