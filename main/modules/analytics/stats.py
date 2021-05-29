import datetime
from django.shortcuts import render
from django.views.generic.base import View
from main.models_addon import Offer
from main.modules.base import BaseView
from main.models_addon.ya_market.order.base import Order, Item, Warehouse
from main.view import Page, get_navbar


def offers_for_last_14_days(included_statuses, user):
    return Offer.objects.filter(

    )


class StatsView(BaseView):
    """Отображение информации о проданных тоарах"""
    context = {
        'title': 'Статистика',
        'page_name': 'Статистика продаж',
    }

    def context_update(self, data: dict):
        self.context = {**data, **self.context}

    def get(self, request):
        local_context = {
            'navbar': get_navbar(request),
        }
        self.context_update(local_context)
        return render(request, Page.stats, self.context)

