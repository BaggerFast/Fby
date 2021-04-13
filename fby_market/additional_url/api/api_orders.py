from django.urls import path

from main.modules.order.order_list import OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list'),
]
