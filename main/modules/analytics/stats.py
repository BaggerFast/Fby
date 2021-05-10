from django.shortcuts import render
from django.views.generic.base import View
from main.view import *


class StatsView(View):
    """Отображение страницы"""
    context = {
        'title': 'Статистика',
    }

    def get(self, request):
        return render(request, Page.stats, self.context)
