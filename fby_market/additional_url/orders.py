from django.urls import path
from main.modules.order.order_list import OrderListView, OrderPageView

urlpatterns = [
    path('', OrderListView.as_view(), name='catalogue_order'),
    path('<int:pk>/', OrderPageView.as_view(), name='order_by_sku'),
]
