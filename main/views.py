import json

import requests
from django.shortcuts import render
from pygments import highlight, lexers, formatters

from fby_market.settings import YA_MARKET_TOKEN, YA_MARKET_CLIENT_ID, YA_MARKET_SHOP_ID
from main.models import Barcode


def catalogue_list(request):
    data = get_data_from_yandex()

    # TODO: save data to DB
    json_object = json.loads(data)
    # save_to_db(json_object)

    formatted_json = json.dumps(json_object, indent=2)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.HtmlFormatter())
    context = {
        'highlight_style': formatters.HtmlFormatter().get_style_defs('.highlight'),
        'content': colorful_json
    }
    return render(request, 'list.html', context)


def get_data_from_yandex():
    headers_str = f'OAuth oauth_token="{YA_MARKET_TOKEN}", oauth_client_id="{YA_MARKET_CLIENT_ID}"'
    headers = {'Authorization': headers_str}
    url = f'https://api.partner.market.yandex.ru/v2/campaigns/{YA_MARKET_SHOP_ID}/offer-mapping-entries.json'
    data = requests.get(url, headers=headers)
    return data.content


def save_to_db(data):
    result_database_objects = {}
    for item in data['result']['offerMappingEntries']:
        offer = item['offer']
        if 'barcodes' in offer.keys():
            barcodes = offer['barcodes']
            result_database_objects['barcodes'] = [Barcode.objects.create(barcode=barcode) for barcode in barcodes]
            offer['barcodes'] = 'SAVED'
