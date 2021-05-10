from django.urls import path
from main.modules import *

urlpatterns = [
    path('', StatsView.as_view(), name='Статистика'),
]
