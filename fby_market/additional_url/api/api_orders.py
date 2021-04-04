from django.urls import path

from main.view.others import orders_list

urlpatterns = [
    path('', orders_list, name='orders_list'),
]
