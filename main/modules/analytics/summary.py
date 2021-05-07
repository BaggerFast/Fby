"""Модуль для рендера страницы аналитики"""
from django.shortcuts import render
from django.views.generic.base import View
import plotly.graph_objects as go
import pandas as pd
import plotly.offline as opy
import plotly.express as px
from main.models_addon.ya_market.offer.base import Offer

from main.view import *


def get_pie_figure():
    """
    Создание круговой диаграммы
    :return: plot class object
    """
    offers = get_data_from_db()
    fig = go.Figure(data=[go.Pie(labels=offers.columns, values=offers.value_counts())])
    return opy.plot(fig, auto_open=False, output_type='div')


def get_data_from_db():
    """
    Функция для получения данных из БД
    :return: Pandas.DataFrame
    """
    offers = Offer.objects.all().values('transportUnitSize', 'user')
    offers = pd.DataFrame(offers)
    return offers


class SummaryView(View):
    """Отображение главной страницы"""
    context = {
        'title': 'Summary',
    }

    def get(self, request):
        self.context['navbar'] = get_navbar(request)
        self.context['graph'] = get_pie_figure()
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
