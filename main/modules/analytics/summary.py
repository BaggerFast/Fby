"""Модуль для рендера страницы аналитики"""
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as opy
from django.shortcuts import render
from django.views.generic.base import View

from main.models_addon.ya_market.order.base import Order
from main.view import *


def get_pie_figure():
    """
    Создание круговой диаграммы
    :return: Объект класса plotly.plot
    """
    offers = get_data_from_db()
    fig = go.Figure(data=[go.Pie(labels=offers.columns, values=offers.value_counts())])

    return opy.plot(fig, auto_open=False, output_type='div')


def get_data_from_db():
    """
    Функция для получения данных из БД
    :return: Объект класса Pandas.DataFrame
    """
    offers = Order.objects.all().values()
    offers = pd.DataFrame(offers)

    return offers


def get_orders_for_current_month(included_statuses, user):
    """
    Возращает заказы за текущий месяц
    :return: Объект класса Django QuerySet
    """
    return Order.objects.filter(
        creationDate__gt=datetime.date.today().replace(day=1),
        status__in=included_statuses,
        user=user
    )


def get_orders_for_previous_month(included_statuses, user):
    """
    Возращает заказы за прошлые месяцы
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


def calculate_total_net_cost(orders):
    """
    Подсчитать себестоимость
    :param orders: Заказы для подсчёта
    :param user: ID пользователя
    :return: Общая себестоимость
    """
    total_net_cost = 0

    for order in orders:
        total_net_cost += order.total_net_price()

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
    Класс второстепенных статов.
    """
    def __init__(self, time='', orders=None):
        """
        Инициализация объекта
        :param time: В какое время подсчитывалось время(прошлый, текущий месяц и т.п.). Строка должна отвечать на вопрос
                     **когда?**
        :param orders: Заказы
        """
        if orders is not None:
            self.time = time
            self.amount = len(orders)
            self.total_cost = f'{calculate_total_cost(orders)}₽'
            self.total_net_cost = f'{calculate_total_net_cost(orders)}₽'
            self.revenue = f'{calculate_revenue(float(self.total_cost[:-1]), float(self.total_net_cost[:-1]))}₽'


class Stat:
    """
    Класс параметра для статистики.
    """

    def __init__(
        self,
        name=None,
        all_orders=None,
        included_statuses=('DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING'),
    ):
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
            SecondaryStats('в этом месяце', filtered_orders[0]),
            SecondaryStats('ранее', filtered_orders[1])
        ]
        self.name = name


class SummaryView(View):
    """Отображение страницы с отчётом"""
    context = {
        'title': 'Отчёт',
    }

    def get(self, request):
        included_statuses = ('DELIVERY', 'DELIVERED', 'PARTIALLY_RETURNED', 'PICKUP', 'PROCESSING')
        orders = [get_orders_for_current_month(included_statuses, request.user), get_orders_for_previous_month(included_statuses, request.user)]

        self.context['navbar'] = get_navbar(request)

        self.context['stats'] = [
            Stat('', [orders[0]], included_statuses),
            Stat('Заказы в доставке', orders, ('DELIVERY', 'PROCESSING', 'PICKUP')),
            Stat('Доставленные в этом месяце заказы', orders, ('DELIVERED', 'PICKUP')),
        ]

        return render(request, Page.summary, self.context)


"""
:param labels: Sectors names
:type labels: list

:param values: Sectors values
:type values: list
"""


def pie(labels=None, values=None):
    """Создание круговой диаграммы"""
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.show()


"""
:param df: Pandas dataframe, that will be displayed on chart
:type df: Pandas df

:param y_axis_name: Name of y axis, x axis automatically set to time 
:type y_axis_name: str

:param range_bottom: Date where chart will begin
:type range_bottom: datetime.datetime

:param range_top: Date where chart will end
:type range_top: datetime.datetime

"""


def time_series(df, y_axis_name, range_bottom, range_top):
    """Создание диаграммы за периуд времени"""
    fig = px.line(df, x='Date', y=y_axis_name, range_x=[range_bottom, range_top])
    fig.show()
