from django.shortcuts import render
from django.views.generic.base import View
from main.views import Page


class MainView(View):
    def get(self, request):
        return render(request, Page.index, None)
