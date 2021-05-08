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


def get_orders_for_month():
    """
    Возращает заказы за текущий месяц
    :return: Объект класса Django QuerySet
    """
    return Order.objects.filter(creationDate__gt=datetime.datetime.now().replace(day=1))


def calculate_total_cost(orders):
    total_cost = 0

    for order in orders:
        total_cost += order.total_price

    return total_cost


class SummaryView(View):
    """Отображение страницы с отчётом"""
    context = {
        'title': 'Summary',
    }

    def get(self, request):
        orders = get_orders_for_month()

        self.context['navbar'] = get_navbar(request)
        self.context['orders_amount'] = len(orders)
        self.context['orders_total_cost'] = f'{calculate_total_cost(orders)}₽'

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
