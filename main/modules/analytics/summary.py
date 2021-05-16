"""Модуль для рендера страницы аналитики"""
import datetime
from django.shortcuts import render
from django.views.generic.base import View
from django.utils import timezone

from main.models_addon import Offer
from main.models_addon.ya_market.order.base import Order
from main.view import Page, get_navbar


def get_orders_for_current_month(included_statuses, user):
    """
    Возвращает заказы за текущий месяц
    :return: Объект класса Django QuerySet
    """
    return Order.objects.filter(
        creationDate__gt=datetime.date.today().replace(day=1),
        status__in=included_statuses,
        user=user
    )


def get_offers(user):
    """
    Возвращает товары пользователя
    :return: Объект класса Django QuerySet
    """
    return Offer.objects.filter(
        user=user
    )


def get_orders_for_previous_month(included_statuses, user):
    """
    Возвращает заказы за прошлые месяцы
    :return: Объект класса Django QuerySet
    """
    return Order.objects.filter(
        creationDate__lt=datetime.date.today().replace(day=1),
        status__in=included_statuses,
        user=user
    )


def calculate_total_cost(orders):
    """
    Подсчитать доход
    :param orders: Заказы для подсчёта
    :return: Общий доход
    """
    total_cost = 0
    for order in orders:
        total_cost += order.total_price
    return total_cost


def calculate_total_net_cost(orders, offers):
    """
    Подсчитать себестоимость
    :param orders: Заказы для подсчёта
    :param user: ID пользователя
    :return: Общая себестоимость
    """
    total_net_cost = 0
    for order in orders:
        total_net_cost += order.total_net_price(offers)
    return total_net_cost


def calculate_revenue(income, net_cost):
    """
    Ф-ия для подсчёта выручки. Рассчитывается по простой формуле *income* - *net_cost*
    :param income: Доход
    :param net_cost: Себестоимость
    :return: Выручка
    """
    return income - net_cost


class SecondaryStats:
    """
    Класс второстепенных stats.
    """

    def __init__(self, time='', orders=None, user=None):
        """
        Инициализация объекта
        :param time: В какое время подсчитывалось время(прошлый, текущий месяц и т.п.). Строка должна отвечать на вопрос
                     **когда?**
        :param orders: Заказы
        """
        if orders is not None:
            self.time = time
            self.amount = len(orders)
            self.total_cost = calculate_total_cost(orders)
            if user:
                self.total_net_cost = calculate_total_net_cost(orders, offers=Offer.objects.filter(user=user))
            else:
                self.total_net_cost = 0
            self.revenue = calculate_revenue(float(self.total_cost), float(self.total_net_cost))


class Stat:
    """
    Класс параметра для статистики.
    """

    def __init__(self, name=None, all_orders=None,
                 included_statuses=('DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING'),
                 user=None):
        """
        Инициализация объекта класса параметр
        :param name: Название параметра
        :param all_orders: Заказы, лист из 2 объектов - заказы за пред. месяц и за тек. месяц соответственно
        :param included_statuses: Какие статусы для фильтра должны быть, если не заданы то берутся стандартные:
            'DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING'
        """
        if len(all_orders) == 1:
            all_orders.append(None)
        filtered_orders = []

        for in_orders in all_orders:
            if in_orders is not None:
                filtered_orders.append(in_orders.filter(status__in=included_statuses))
            else:
                filtered_orders.append(None)

        self.secondary_stats = [
            SecondaryStats('в этом месяце', filtered_orders[0], user),
            SecondaryStats('ранее', filtered_orders[1], user)
        ]
        self.name = name


class SummaryView(View):
    context = {}

    def context_update(self, data: dict):
        self.context = {**data, **self.context}

    """Отображение страницы с отчётом"""

    def get(self, request):
        included_statuses = ('DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING')
        user = request.user

        orders = [get_orders_for_current_month(included_statuses, user),
                  get_orders_for_previous_month(included_statuses, user)]

        offers = get_offers(user)

        local_context = {
            'navbar': get_navbar(request),
            'stats': [
                Stat('', [orders[0]], included_statuses),
                Stat('Заказы в доставке', orders, ('DELIVERY', 'PROCESSING', 'PICKUP'), user),
                Stat('Доставленные в этом месяце заказы',
                     [orders[0], orders[1].filter(statusUpdateDate=timezone.now())],
                     ('DELIVERED', 'PICKUP'),
                     user)
            ],
            'title': 'Отчёт',
            'delisted_offers_amount': len(offers.filter(availability='DELISTED'))
        }

        self.context_update(local_context)

        return render(request, Page.summary, self.context)
