import json
import requests
from django.shortcuts import render
from pygments import highlight, lexers, formatters
from fby_market.settings import YA_MARKET_TOKEN, YA_MARKET_CLIENT_ID, YA_MARKET_SHOP_ID
from main.models.offer_save import OfferPattern
from main.models.base import Offer


def catalogue_list(request):
    json_object = get_catalogue_from_file("data_file.json")
    save_to_db(json_object)

    formatted_json = json.dumps(json_object, indent=2, ensure_ascii=False)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.HtmlFormatter())
    context = {
        'highlight_style': formatters.HtmlFormatter().get_style_defs('.highlight'),
        'content': colorful_json,
    }
    return render(request, 'list.html', context)


def offer_by_sku(request, sku):
    data_object = Offer.objects.get(shop_sku=sku)
    json_object = json.dumps(data_object, default=lambda o:o.__dict__, sort_keys=True, indent=2, ensure_ascii=False)

    colorful_json = highlight(json_object, lexers.JsonLexer(), formatters.HtmlFormatter())
    context = {
        'highlight_style': formatters.HtmlFormatter().get_style_defs('.highlight'),
        'content': colorful_json,
    }
    return render(request, 'list.html', context)

def account_login(request):
    pass

def account_register(request):
    pass

def offer_by_sku_edit(request):
    pass



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
