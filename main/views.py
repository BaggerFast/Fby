import ast
import json

import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from fby_market.settings import YA_MARKET_TOKEN, YA_MARKET_CLIENT_ID, YA_MARKET_SHOP_ID
from main.models.base import Offer
from main.models.offer_save import OfferPattern
from main.serializers import OfferSerializer


@api_view(['GET'])
def catalogue_list(request):
    page = request.GET.get('page')
    amount = 5
    data_objects = data_paginator(Offer.objects.all(), amount, page)
    serializer = OfferSerializer(data_objects, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def offer_by_sku(request, sku):
    """
    Обработчик получения данных об одном товаре

    .. todo::
       Написать обработку POST-запроса
    """
    if request.method == 'GET':
        data = get_object_or_404(Offer, shop_sku=sku)
        serializer = OfferSerializer(data)
        return Response(serializer.data)


@csrf_exempt
def offer_by_sku_edit(request, sku):
    input_object = request.body

    dict_str = input_object.decode("UTF-8")
    data_object = ast.literal_eval(dict_str)
    print(data_object)
    # ToDo DB.2 (edit)


def data_paginator(data, amount, page):
    p = Paginator(data, amount)
    try:
        return p.page(page)
    except EmptyPage:
        return p.page(1)
    except PageNotAnInteger:
        return p.page(1)


def get_catalogue_from_ym():
    """
    Загрузка каталога из YandexMarket и сохранение в файл data_file.json
    """
    data = get_data_from_yandex()
    json_object = json.loads(data)
    while 'nextPageToken' in json_object['result']['paging']:  # если страница не последняя, читаем следующую
        next_page_token = json_object['result']['paging']['nextPageToken']
        next_json_object = json.loads(get_data_from_yandex(next_page_token))
        json_object['result']['offerMappingEntries'] += next_json_object['result']['offerMappingEntries']
        json_object['result']['paging'] = next_json_object['result']['paging']
    with open("data_file.json", "w") as write_file:
        json.dump(json_object, write_file, indent=2, ensure_ascii=False)
    return json_object


def get_catalogue_from_file(file):
    """
    Загрузка каталога из файла file
    """
    with open(file, "r", encoding="utf-8") as read_file:
        json_object = json.load(read_file)
    return json_object


def get_data_from_yandex(next_page_token=None):
    headers_str = f'OAuth oauth_token="{YA_MARKET_TOKEN}", oauth_client_id="{YA_MARKET_CLIENT_ID}"'
    headers = {'Authorization': headers_str}
    url = f'https://api.partner.market.yandex.ru/v2/campaigns/{YA_MARKET_SHOP_ID}/offer-mapping-entries.json'
    if next_page_token:
        url += f'?page_token={next_page_token}'
    data = requests.get(url, headers=headers)
    return data.content


def save_to_db(data):
    data = OfferPattern(json=data['result']['offerMappingEntries'])
    data.save()
