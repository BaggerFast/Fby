from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.views import View
import itertools


class BaseView(LoginRequiredMixin, View):
    """
    Базовый класс для отображения каталога
    """
    context = {}
    request = None

    def context_update(self, data: dict):
        self.context = {**data, **self.context}

    def save_models(self, request: HttpRequest) -> HttpResponse:
        for model in self.models_to_save:
            if not model(request=request).save():
                break
        return self.get(request=request)

    def search_algorithm(self, keywords, objects):
        if not len(keywords):
            return objects
        scores = {}
        for item, keyword in itertools.product(objects, keywords):
            for field in self.fields:
                attr = getattr(item, field)
                if attr is not None and keyword in str(attr).lower():
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
