import json
from django.shortcuts import render
from pygments import highlight, lexers, formatters
from rest_framework import generics

from main.models import Offer
from main.serializers.offer_price import OfferSerializer
from main.yandex.request_yandex import OrderList


class OfferList(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()


class OfferDetails(generics.RetrieveAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    lookup_field = 'id'


class OfferEdit(generics.UpdateAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    lookup_field = 'shopSku'


def get_json_data_from_file(file):
    """
    Загрузка данных из файла file
    """
    with open(file, "r", encoding="utf-8") as read_file:
        json_object = json.load(read_file)
    return json_object


def orders_list(request):
    json_object = get_json_data_from_file("orders_file.json")

    formatted_json = json.dumps(json_object, indent=2, ensure_ascii=False)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.HtmlFormatter())
    context = {
        'highlight_style': formatters.HtmlFormatter().get_style_defs('.highlight'),
        'content': colorful_json,
    }

    # OrderPattern(json=json_object['result']['orders']).save()
    OrderList().save()

    return render(request, 'orders.html', context)







