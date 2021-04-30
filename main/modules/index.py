from django.shortcuts import render
from django.views.generic.base import View
from main.view import *


class MainView(View):
    """отображение главной страницы"""
    context = {'title': 'Main'}

    @staticmethod
    def get(request):
        return render(request, Page.index, {'navbar': get_navbar(request)})
