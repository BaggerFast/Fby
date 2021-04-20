import json
import sqlite3
import pandas as pd
from django.shortcuts import render
from pygments import highlight, lexers, formatters
from main.models_addon import Offer
from main.models_addon.save_dir import OfferPattern, OrderPattern, PricePattern, OfferReportPattern
from main.ya_requests.request import UpdateOfferList


def get_json_data_from_file(file: str) -> dict:
    """Загрузка данных из файла file."""
    with open(file, "r", encoding="utf-8") as read_file:
        json_object = json.load(read_file)
    return json_object


def temp_page(request):
    """
    Временная страница для отладки десериализации.

    Будет удалена перед окончательным релизом.
    """
    offers_list = [Offer.objects.all().get(shopSku='04E129620')]
    # Offer.objects.filter(manufacturer='Филиппс').update(manufacturer='Филипс')
    update_list = UpdateOfferList(offers_list)
    update_list.update_offers()
    errors = update_list.errors
    success = update_list.success

    json_object = success

    # OfferList().save_json_to_file("offer_data.json")
    # json_object = get_json_data_from_file("offer_data.json")

    formatted_json = json.dumps(json_object, indent=2, ensure_ascii=False)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.HtmlFormatter())
    context = {
        'highlight_style': formatters.HtmlFormatter().get_style_defs('.highlight'),
        'content': colorful_json,
    }

    return render(request, 'temp.html', context)


def save_db_from_files(request):
    """Восстановление бд из файлов"""
    json_object_offer = get_json_data_from_file("json_data/offer_data.json")
    OfferPattern(json=json_object_offer['result']['offerMappingEntries']).save(request.user)
    json_object_order = get_json_data_from_file("json_data/order_data.json")
    OrderPattern(json=json_object_order['result']['orders']).save(request.user)
    json_object_prise = get_json_data_from_file("json_data/price_data.json")
    PricePattern(json=json_object_prise['result']['offers']).save(request.user)
    json_object_report = get_json_data_from_file("json_data/offer_report_data.json")
    OfferReportPattern(json=json_object_report['result']['shopSkus']).save(request.user)

    return render(request, 'save_db.html')


def db_to_exel(sql_script="SELECT * FROM main_offer", db_name='database.xlsx'):
    pd.read_sql_query(sql=sql_script, con=sqlite3.connect('db.sqlite3')).to_excel(db_name)
