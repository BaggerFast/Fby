"""Модуль для рендера страницы аналитики"""
import datetime
from django.shortcuts import render
from django.views.generic.base import View
from main.models_addon import Offer
from main.models_addon.ya_market.order.base import Order, Item, Warehouse
from main.view import Page, get_navbar


def orders_for_current_month(included_statuses, user):
    """
    Возвращает заказы за текущий месяц
    :return: Объект класса Django QuerySet
    """
    return Order.objects.filter(
        creationDate__gt=datetime.date.today().replace(day=1),
        status__in=included_statuses,
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

    def __init__(self, time='', orders=None, request=None):
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
            if request:
                self.total_net_cost = calculate_total_net_cost(orders, offers=Offer.objects.filter(user=request.user))
            else:
                self.total_net_cost = 0
            self.revenue = calculate_revenue(float(self.total_cost), float(self.total_net_cost))


class Stat:
    """
    Класс параметра для статистики.
    """

    def __init__(self, name=None, all_orders=None,
                 included_statuses=('DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING'),
                 request=None):
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
            SecondaryStats('в этом месяце', filtered_orders[0], request=request),
            SecondaryStats('ранее', filtered_orders[1], request=request)
        ]
        self.name = name


def get_warehouse_items(orders, warehouse_id: list):
    """
    Получить товары со складов.
    :param warehouse_id: Лист ИД складов
    :return: Объект класса Django QuerySet
    """
    warehouse_items = []

    for order in orders:
        # items = order.get_items.objects.filter(warehouse__in=warehouse_id)
        items = order.get_items.filter(warehouse__in=warehouse_id)
        warehouse_items.append(*items)

    return warehouse_items


def calculate_item_total_cost(items):
    """
    Подсчитать доход
    :param orders: Заказы для подсчёта
    :return: Общий доход
    """
    total_cost = 0
    for item in items:
        total_cost += item.per_item_price
    return total_cost


class SummaryView(View):
    context = {}

    def context_update(self, data: dict):
        self.context = {**data, **self.context}

    """Отображение страницы с отчётом"""

    def get(self, request):
        included_statuses = ('DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING')
        orders = [orders_for_current_month(included_statuses, user=request.user),
                  get_orders_for_previous_month(included_statuses, user=request.user)]
        warehouse_items = get_warehouse_items(orders[1], Warehouse.objects.all())
        local_context = {
            'navbar': get_navbar(request),
            'stats': [
                Stat('', [orders[0]], included_statuses),
                Stat('Заказы в доставке', orders, ('DELIVERY', 'PROCESSING', 'PICKUP'), request=request),
                Stat('Доставленные в этом месяце заказы', orders, ('DELIVERED', 'PICKUP'), request=request),
            ],
            'title': 'Отчёт',
            'warehouse_items_amount': len(warehouse_items),
            'warehouse_items_cost': calculate_item_total_cost(warehouse_items),
        }
        self.context_update(local_context)
        return render(request, Page.summary, self.context)
