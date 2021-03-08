import json
import requests
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from pygments import highlight, lexers, formatters
from fby_market.settings import YA_MARKET_TOKEN, YA_MARKET_CLIENT_ID, YA_MARKET_SHOP_ID
from main.models.offer_save import OfferPattern
from main.models.base import Offer
import ast
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import modelform_factory
from django.contrib.auth.models import User


def catalogue_list(request):
    page = request.GET.get('page')
    amount = 5  # Количество оферов на странице
    data_objects = data_paginator(Offer.objects.all(), amount,
                                  page)  # Если запрашивает несуществующую страницу, то вернет первую
    json_object = serializers.serialize('json', data_objects, sort_keys=True, indent=2, ensure_ascii=False)

    colorful_json = highlight(json_object, lexers.JsonLexer(), formatters.HtmlFormatter())
    context = {
        'highlight_style': formatters.HtmlFormatter().get_style_defs('.highlight'),
        'content': colorful_json,
    }
    return render(request, 'list.html', context)


def offer_by_sku(request, sku):
    # GET
    return render(request, 'list.html', make_context(make_json(Offer.objects.get(shop_sku=sku))))


def make_json(data_object):
    return json.dumps(data_object, default=lambda o: o.__dict__, sort_keys=True, indent=2, ensure_ascii=False)


def make_context(json_object):
    return {
        'highlight_style': formatters.HtmlFormatter().get_style_defs('.highlight'),
        'content': highlight(json_object, lexers.JsonLexer(), formatters.HtmlFormatter()),
    }


@csrf_exempt
def account_login(request):
    input_object = request.body
    dict_str = input_object.decode("UTF-8")
    data_object = ast.literal_eval(dict_str)
    print(data_object)
    user = authenticate(request, username=data_object['username'], password=data_object['password'])
    if user is not None:
        login(request, user)
        print('Success')
    else:
        print('Bad')


@csrf_exempt
def account_register(request):
    # POST
    input_object = request.body
    dict_str = input_object.decode("UTF-8")
    data_object = ast.literal_eval(dict_str)
    keys = list(data_object.keys())
    print(keys)
    form = modelform_factory(User, fields=keys)
    current_form = form(data=data_object)
    if current_form.is_valid():
        current_form.save()
        print('OK')
    else:
        print('NO')


@csrf_exempt
def offer_by_sku_edit(request, sku):
    input_object = request.body

    dict_str = input_object.decode("UTF-8")
    data_object = ast.literal_eval(dict_str)
    print(data_object)
    # ToDo DB.2 (edit)

    # json_object == make_json(Offer.objects.get(shop_sku=sku)) сравнить


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
