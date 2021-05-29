from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
import itertools


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
    def get_item_display_name(item, field):
        get_display_name = "get_{}_display".format(field)
        if hasattr(item, get_display_name):
            return getattr(item, get_display_name)()
        else:
            return None

    def search_algorithm(self, keywords, objects):
        if not len(keywords):
            return objects
        scores = {}
        for item, keyword in itertools.product(objects, keywords):
            for field in self.fields:
                attr_display = self.get_item_display_name(item, field)
                attr_actual = getattr(item, field)
                if attr_actual is not None and \
                    keyword in str(attr_display).lower() or \
                    keyword in str(attr_actual).lower():
                    if item not in scores:
                        scores[item] = 0
                    scores[item] += 1
                    break
        return sorted(scores, key=scores.get, reverse=True)

    def sort_object(self, offer, filter_types) -> list:
        self.context_update({
            "checked": self.filtration.checked_filters_from_request(self.request, filter_types),
            "input": self.request.GET.get('input', '').strip(),
        })

        if self.request.GET.get("no_search"):
            self.context_update({'search': False})
            return offer

        keywords = self.request.GET.get('input', '').lower().strip().split()
        filters = self.filtration.filters_from_request(self.request, filter_types)
        objects = self.search_algorithm(keywords, self.filtration.filter_items(offer, filters))
        was_searching_used = len(keywords) != 0
        if not was_searching_used:
            filter_values = [j for sub in filters.values() for j in sub]
            if len(filter_values):
                was_searching_used = True
        self.context_update({'search': was_searching_used})
        return objects

    def end_it(self) -> HttpResponse:
        pass
