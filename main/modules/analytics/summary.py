"""Модуль для рендера страницы аналитики"""
from django.contrib import messages
from django.db.models import Q
import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from main.models_addon.ya_market import Order
from main.modules.base import BaseView
from main.view import Page, Navbar
from main.modules.analytics.addition import Stat


class SummaryView(BaseView):
    context = {
        'title': 'Отчёт',
    }
    included_statuses = ['DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING']

    """Отображение страницы с отчётом"""
    def get(self, request):
        orders = Order.objects.filter(user=self.request.user)
        data_today = datetime.date.today().replace(day=1)
        if not orders:
            messages.success(self.request, 'Каталог заказов пуст, статистика не возможна')
            return redirect(reverse('catalogue_order'))
        filter_cur_month = Q(creationDate__gt=data_today, status__in=self.included_statuses)
        filter_prev_month = Q(creationDate__lt=data_today, status__in=self.included_statuses)
        orders = [*[orders.filter(fill).prefetch_related('items').prefetch_related('items__prices')
                    for fill in [filter_cur_month, filter_prev_month]]]
        local_context = {
            'navbar': Navbar(request).get(),
            'stats': [
                Stat(name='Заказы и доставка', all_orders=[orders[0]], included_statuses=self.included_statuses),
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
