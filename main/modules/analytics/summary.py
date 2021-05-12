"""Модуль для рендера страницы аналитики"""

from django.shortcuts import render
from django.views.generic.base import View
from main.view import Page, get_navbar
from main.modules.analytics.addition import *


class SummaryView(View):
    context = {}

    def context_update(self, data: dict):
        self.context = {**data, **self.context}

    """Отображение страницы с отчётом"""

    def get(self, request):
        included_statuses = ('DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING')
        orders = [orders_for_current_month(included_statuses, user=request.user),
                  get_orders_for_previous_month(included_statuses, user=request.user)]
        local_context = {
            'navbar': get_navbar(request),
            'stats': [
                Stat('', [orders[0]], included_statuses),
                Stat('Заказы в доставке', orders, ('DELIVERY', 'PROCESSING', 'PICKUP'), request=request),
                Stat('Доставленные в этом месяце заказы', orders, ('DELIVERED', 'PICKUP'), request=request),
            ],
            'title': 'Отчёт',
        }
        self.context_update(local_context)
        return render(request, Page.summary, self.context)
