from django.shortcuts import render
from django.views.generic.base import View
from main.views import Page, get_navbar


class MainView(View):
    """отображение гланой страницы"""

    context = {}

    def get(self, request):
        self.context['navbar'] = get_navbar(request)
        return render(request, Page.index, self.context)
