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

    def reformat_order(self, order) -> list:
        def order_search(orders) -> list:
            def search_algorithm():
                if not len(keywords):
                    return orders
                scores = {}
                for item in orders:
                    for keyword in keywords:
                        for field in fields:
                            attr = getattr(item, field)
                            if attr is not None and keyword in str(attr).lower():
                                if item not in scores:
                                    scores[item] = 0
                                scores[item] += 1
                                break
                return sorted(scores, key=scores.get, reverse=True)

            search = self.request.GET.get('input', '').lower()
            fields = ['order_id', 'status', 'statusUpdateDate', 'deliveryRegion', 'price']
            keywords = search.strip().split()
            objects = search_algorithm()
            self.context_update({'search': bool(len(search)), 'count': len(objects)})
            return objects

        return order_search(order)

    def post(self, request) -> HttpResponse:
        for model in self.models_to_save:
            if not model(request=request).save():
                break
        return self.get(request=request)

    def get(self, request) -> HttpResponse:
        local_context = {
            'navbar': get_navbar(request),
            'orders': self.reformat_order(Order.objects.filter(user=request.user)),
            'table': ["Номер заказа", "Дата заказа", "Цена, ₽", "Статус"]
        }
        print(31)
        self.context_update(local_context)
        return render(request, Page.order, self.context)


class OrderPageView(BaseView):
    context = {'title': 'Order', 'page_name': 'Карточка заказа'}

    def get(self, request, pk) -> HttpResponse:
        order = get_object_or_404(Order, pk=pk)
        local_context = {
            'navbar': get_navbar(request),
            'order': order,
        }
        self.context_update(local_context)
        return render(request, Page.order_page, self.context)
