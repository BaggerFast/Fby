import json
import sqlite3
import pandas as pd
from django.shortcuts import render
from pygments import highlight, lexers, formatters
from main.models.save_dir import OfferPattern, OrderPattern, PricePattern, OfferReportPattern
from main.yandex.request import OfferUpdate


def get_json_data_from_file(file: str) -> dict:
    """Загрузка данных из файла file."""
    with open(file, "r", encoding="utf-8") as read_file:
        json_object = json.load(read_file)
    return json_object


def orders_list(request):
    """Временная страница для отладки десериализации"""
    json_object = OfferUpdate('04E129620').answer()

    # json_object = get_json_data_from_file("order_data.json")

    formatted_json = json.dumps(json_object, indent=2, ensure_ascii=False)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.HtmlFormatter())
    context = {
        'highlight_style': formatters.HtmlFormatter().get_style_defs('.highlight'),
        'content': colorful_json,
    }
    # OfferReportPattern(json=json_object['result']['shopSkus']).save(request.user)

    return render(request, 'orders.html', context)


def save_db_from_files(request):
    """Восстановление бд из файлов"""
    json_object_offer = get_json_data_from_file("offer_data.json")
    OfferPattern(json=json_object_offer['result']['offerMappingEntries']).save(request.user)
    json_object_order = get_json_data_from_file("order_data.json")
    OrderPattern(json=json_object_order['result']['orders']).save(request.user)
    json_object_prise = get_json_data_from_file("price_data.json")
    PricePattern(json=json_object_prise['result']['offers']).save(request.user)
    json_object_report = get_json_data_from_file("offer_report_data.json")
    OfferReportPattern(json=json_object_report['result']['shopSkus']).save(request.user)

    return render(request, 'save_db.html')


def db_to_exel():
    db_set = sqlite3.connect("db.sqlite3")
    db_frame = pd.read_sql_query("SELECT * FROM main_offer", db_set)
    db_frame.to_excel('database.xlsx')
