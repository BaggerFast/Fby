from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
import itertools

from typing import List

from main.models_addon.ya_market import Offer


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

    # todo fix algorithm of all functions under me
    @staticmethod
    def get_item_display_name(item, field: str):
        get_display_name = f"get_{field}_display"
        if hasattr(item, get_display_name):
            return getattr(item, get_display_name)()
        else:
            return None

    def search_algorithm(self, keywords: List[str], objects: List[Offer]) -> List[Offer]:
        if not len(keywords):
            return objects
        search_results = []
        for item, keyword in itertools.product(objects, keywords):
            for field in self.fields:
                attr_display = str(self.get_item_display_name(item, field)).lower()
                attr_actual = str(getattr(item, field)).lower()
                if attr_actual and keyword in attr_display or keyword in attr_actual:
                    search_results.append(item)
                    pprint(search_results)
                    break
        return search_results

    def sort_object(self, offers, filter_types):
        self.context_update({
            "checked": self.filtration.checked_filters_from_request(self.request, filter_types),
            "input": self.request.GET.get('input', '').strip(),
        })

        if self.request.GET.get("no_search"):
            self.context_update({'search': False})
            return offers

        keywords = self.request.GET.get('input', '').lower().strip().split('|')
        filters = self.filtration.filters_from_request(self.request, filter_types)
        objects = self.search_algorithm(keywords, self.filtration.filter_items(offers, filters))
        pprint(objects)
        was_searching_used = len(keywords) != 0
        if not was_searching_used:
            filter_values = [j for sub in filters.values() for j in sub]
            if len(filter_values):
                was_searching_used = True
        self.context_update({'search': was_searching_used})
        return objects

    def end_it(self) -> HttpResponse:
        pass
