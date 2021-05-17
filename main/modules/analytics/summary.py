"""Модуль для рендера страницы аналитики"""
from django.contrib import messages
from django.db.models import Q
import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from main.models_addon.ya_market import Order
from main.modules.base import BaseView
from main.view import Page, get_navbar
from main.modules.analytics.addition import Stat


class SummaryView(BaseView):
    context = {
        'title': 'Отчёт',
    }

    """Отображение страницы с отчётом"""

    def get(self, request):
        included_statuses = ('DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING')
        orders = Order.objects.filter(user=self.request.user)
        data_today = datetime.date.today().replace(day=1)
        if not orders:
            messages.success(self.request, 'Каталог заказов пуст, статистика не возможна')
            return redirect(reverse('orders_list'))
        filter_cur_month = Q(creationDate__gt=data_today, status__in=included_statuses)
        filter_prev_month = Q(creationDate__lt=data_today, status__in=included_statuses)
        orders = [orders.filter(filter_cur_month), orders.filter(filter_prev_month)]

        local_context = {
            'navbar': get_navbar(request),
            'stats': [
                Stat(name='Заказы и доставка', all_orders=[orders[0]], included_statuses=included_statuses),
                Stat(name='Заказы в доставке', all_orders=orders,
                     included_statuses=('DELIVERY', 'PROCESSING', 'PICKUP'),
                     request=request),
                Stat(name='Доставленные в этом месяце заказы', all_orders=orders, included_statuses=('DELIVERED',
                                                                                                     'PICKUP'),
                     request=request),
            ],
        }
        self.context_update(local_context)
        return render(request, Page.summary, self.context)
