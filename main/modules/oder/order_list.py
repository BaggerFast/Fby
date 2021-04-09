from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from main.models import Order
from main.view import get_navbar, Page
from main.yandex import OrderList


class CatalogueView(LoginRequiredMixin, View):
    """отображение каталога"""
    context = {'title': 'Order', 'page_name': 'Заказы'}
    models_to_save = [OrderList]

    def context_update(self, data: dict):
        self.context = {**self.context, **data}

    def post(self, request) -> HttpResponse:
        for model in self.models_to_save:
            if not model().save(request=request):
                break
        return self.get(request=request)

    def get(self, request) -> HttpResponse:
        order = Order.objects.filter(user=request.user)
        local_context = {
            'navbar': get_navbar(request),
            'count': order.count(),
            'orders': order,
            'table': ["Номер заказа и состав", "Дата заказа", "Цена, ₽", "Статус"]
        }
        self.context_update(local_context)

        return render(request, Page.order, self.context)

    # def offer_search(self, offers) -> list:
    #     search = self.request.GET.get('input', '').lower()
    #     self.context['search'] = True if len(search) else False
    #     fields = ['name', 'description', 'shopSku', 'category', 'vendor']
    #     objects = []
    #     for item in offers:
    #         try:
    #             for field in fields:
    #                 if search in getattr(item, field).lower():
    #                     objects.append(item)
    #                     break
    #         except:
    #             pass
    #     self.context['count'] = len(objects)
    #     return objects
