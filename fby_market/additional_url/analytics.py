from django.urls import path
from main.modules import *

urlpatterns = [
    path('', SummaryView.as_view(), name='Сводка'),
]
