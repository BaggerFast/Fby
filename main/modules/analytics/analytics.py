from django.shortcuts import render
from django.views.generic.base import View
from main.view import *


class SummaryView(View):
    """отображение главной страницы"""
    context = {'title': 'Summary'}

    def get(self, request):
        self.context['navbar'] = get_navbar(request)
        return render(request, Page.summary, self.context)
