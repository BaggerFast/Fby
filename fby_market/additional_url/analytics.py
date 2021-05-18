from django.urls import path
from main.modules import SummaryView

urlpatterns = [
    path('', SummaryView.as_view(), name='summary'),
]
