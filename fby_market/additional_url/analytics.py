from django.urls import path
from main.modules import *

urlpatterns = [
    # path('compare', price_compare)
    path('', SummaryView.as_view(), name='summary'),
]
