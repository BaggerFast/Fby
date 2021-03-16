from django.shortcuts import render
from django.views.generic.base import View

from main.views import *


class MainView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {
            'navbar': None
        }

    def get(self, request):
        return render(request, Page.index, self.context)
