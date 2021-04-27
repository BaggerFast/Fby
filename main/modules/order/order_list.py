from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from main.models_addon import Order
from main.view import get_navbar, Page
from main.ya_requests import OrderList
from main.modules.base import BaseView


class OrderListView(BaseView):
    """отображение каталога"""
    context = {'title': 'Order', 'page_name': 'Заказы'}
    models_to_save = [OrderList]

    def post(self, request) -> HttpResponse:
        for model in self.models_to_save:
            if not model(request=request).save():
                break
        return self.get(request=request)

    def get(self, request) -> HttpResponse:
        order = Order.objects.filter(user=request.user)
        local_context = {
            'navbar': get_navbar(request),
            'orders': order,
            'table': ["Номер заказа", "Дата заказа", "Цена, ₽", "Статус"]
        }
        print(31)
        self.context_update(local_context)
        return render(request, Page.order, self.context)


class OrderPageView(BaseView):
    context = {'title': 'Order', 'page_name': 'Заказы'}

    def get(self, request, pk) -> HttpResponse:
        order = get_object_or_404(Order, pk=pk)
        local_context = {
            'navbar': get_navbar(request),
            'order': order,
        }
        self.context_update(local_context)
        return render(request, Page.order_page, self.context)
