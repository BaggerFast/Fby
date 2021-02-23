import json

import requests
from django.shortcuts import render
from pygments import highlight, lexers, formatters

from fby_market.settings import YA_MARKET_TOKEN, YA_MARKET_CLIENT_ID, YA_MARKET_SHOP_ID
from main.models.offer_save import OfferPattern


def catalogue_list(request):
    json_object = get_catalogue_from_file("data_file.json")
    # TODO: save data to DB
    save_to_db(json_object)

    formatted_json = json.dumps(json_object, indent=2, ensure_ascii=False)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.HtmlFormatter())
    context = {
        'highlight_style': formatters.HtmlFormatter().get_style_defs('.highlight'),
        'content': colorful_json,
    }
    return render(request, 'list.html', context)


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
    with open(file, "r") as read_file:
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


"""
    of = Offer.objects.create()
    of.name = "Масляный фильтр VOLKSWAGEN 04e115561h"
    of.shop_sku = "04e115561h"
    of.category = "Масляные фильтры"
    of.manufacturer = "Фольцваген"
    of.vendor = "VOLKSWAGEN"
    of.vendor_code = "04e115561h"
    of.description = "Применение: для моторных масел\nПодходит для: Audi A5, Audi A3, Audi A1, Audi Q3, Audi S5, Audi S3, Audi A4, Audi Q2, Audi S4, Seat Leon, Seat Ibiza, Seat Toledo, Seat Alhambra, Seat Ateca, Seat Mii, Skoda Kodiaq, Skoda Superb, Skoda Rapid, Skoda Octavia, Skoda Fabia, Skoda Yeti, Skoda Citigo, Volkswagen Caddy, Volkswagen Jetta, Volkswagen Golf, Volkswagen Beetle, Volkswagen CC, Volkswagen Touran, Volkswagen Polo, Volkswagen Up, Volkswagen Passat, Volkswagen Scirocco, Volkswagen Sharan, Volkswagen Tiguan"
    # of.certificate = 0  " по умолчание null "
    of.availability = "ACTIVE"
    of.transport_unit_size = 1
    of.min_shipment = 1
    of.quantum_of_supply = 1
    of.supply_schedule_days.add(SupplyScheduleDays(
        offer=of,
        supply_schedule_day="TUESDAY"), bulk=False
    )
    of.delivery_duration_days = 1
    # of.box_count = 0  " по умолчание null "
    of.manufacturer_countries.add(ManufacturerCountry(offer=of, name="Германия"), ManufacturerCountry(offer=of, name="Россия"), bulk=False )
    of.weight_dimensions = WeightDimension(
        offer=of,
        length=8,
        width=6,
        height=20,
        weight=0.3
    )
    of.urls.add(Url(
        offer=of,
        url="https://yadi.sk/d/TipaN1TOmS0STw"),
        bulk=False
    )
    of.barcodes.add(Barcode(
        offer=of,
        barcode="4607012404879"), bulk=False
    )
    of.timing.add(Timing(
        offer=of,
        time_period=5,
        time_unit="YEAR",
        comment="",
        timing_type=1), bulk=False
    )
    of.customs_commodity_code.add(CustomsCommodityCode(
        offer=of,
        code=1), bulk=False
    )
    of.processing_state.add(ProcessingState(
        offer=of,
        status="NEED_INFO"), bulk=False
    )
    for i in of.processing_state.all():
        i.notes.add(ProcessingStateNote(
            processing_state=i,
            note_type="NO_PARAMETERS_IN_SHOP_TITLE",
            payload='{"itemsAsString":"Объём","items":["Объём"]}'), bulk=False
        )
    of.mapping.add(Mapping(
        offer=of,
        market_sku=561833112,
        model_id=5,
        category_id=90442,
        mapping_type=""), bulk=False
    )
    of.save()
"""
