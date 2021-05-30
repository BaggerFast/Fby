from django.shortcuts import render
from django.views.generic.base import View
from main.view import Navbar, Page


class FaqView(View):
    """отображение страницы FAQ"""
    context = {'title': 'FAQ', 'page_name': 'FAQ'}

    def get(self, request):
        self.context['navbar'] = Navbar(request).get()
        return render(request, Page.faq, self.context)
