import re
from typing import List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from main.modules.search import search_algorithm


class BaseView(LoginRequiredMixin, View):
    """
    Базовый класс для отображения каталога
    """
    context = dict()
    request = None

    def context_update(self, data: dict):
        self.context.update(data)

    def save_models(self, request: HttpRequest, name) -> HttpResponse:
        for model in self.models_to_save:
            if not model(request=request).save():
                break
        return redirect(reverse(name))

    def sort_object(self, offers, filter_types):
        self.context_update({
            "checked": self.filtration.checked_filters_from_request(self.request, filter_types),
            "input": self.request.GET.get('input', '').strip(),
        })

        if self.request.GET.get("no_search"):
            self.context_update({'search': False})
            return offers

        keywords = self.request.GET.get('input', '')
        filters = self.filtration.filters_from_request(self.request, filter_types)
        objects = search_algorithm(keywords, self.filtration.filter_items(offers, filters), self.fields)

        if len(keywords) != 0:
            self.context_update({'search': True})
        else:
            self.context_update({'search': False})

        return objects

    def end_it(self) -> HttpResponse:
        pass
