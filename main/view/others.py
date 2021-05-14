import json
import sqlite3
import pandas as pd
from django.http import HttpRequest
from django.shortcuts import render
from main.models_addon.save_dir import OfferPattern, OrderPattern, PricePattern, OfferReportPattern


def save_db_from_files(request: HttpRequest):
    def get_json_data_from_file(file: str) -> dict:
        """Загрузка данных из файла file."""
        file = f'json_data/{file}.json'
        with open(file, "r", encoding="utf-8") as read_file:
            return json.load(read_file)['result']

    """Восстановление бд из файлов"""
    context = {
        # OfferPattern: {'file': "offer_data", 'attrs': 'offerMappingEntries'},
        OrderPattern: {'file': "order_data", 'attrs': 'orders'},
        # PricePattern: {'file': "price_data", 'attrs': 'offers'},
        # OfferReportPattern: {'file': "offer_report_data", 'attrs': 'shopSkus'}
    }
    for pattern, attrs in context.items():
        pattern(json=get_json_data_from_file(file=attrs['file'])[attrs['attrs']]).save(user=request.user)

    return render(request, 'save_db.html')


def db_to_exel(sql_script="SELECT * FROM main_offer"):
    pd.read_sql_query(sql=sql_script, con=sqlite3.connect("db.sqlite3")).to_excel('database.xlsx')
