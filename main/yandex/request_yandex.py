"""Формирование запросов в YM для получения данных и сохранения их в БД"""
import time

from django.contrib import messages

from fby_market.settings import YaMarket
import requests

from main.models import Price, Offer
from main.models.save_dir import *


class Requests:
    """Базовый класс для получения данных и сохранения в БД"""

    PARAMS: dict = None  # параметры запроса в формате json (для post-запросов)

    errors = {
        206: "Запрос выполнен частично.",
        400: "Запрос невалидный.",
        401: "В запросе не указаны авторизационные данные.",
        403: "Неверны авторизационные данные, указанные в запросе, или запрещен доступ к запрашиваемому ресурсу.",
        404: "Запрашиваемый ресурс не найден.",
        405: "Запрашиваемый метод для указанного ресурса не поддерживается.",
        415: "Запрашиваемый тип контента не поддерживается методом.",
        420: "Превышено ограничение на доступ к ресурсу.",
        500: "Внутренняя ошибка сервера. Попробуйте вызвать метод через некоторое время. При повторении ошибки"
             " обратитесь в службу технической поддержки Маркета.",
        503: "Сервер временно недоступен из-за высокой загрузки. Попробуйте вызвать метод через некоторое время.",
    }

    def __init__(self, json_name: str, base_context_name: str, name: str):
        self.url = f'https://api.partner.market.yandex.ru/v2/campaigns/{YaMarket.SHOP_ID}/{json_name}.json'
        self.headers_str = f'OAuth oauth_token="{YaMarket.TOKEN}", oauth_client_id="{YaMarket.CLIENT_ID}"'
        self.headers = {'Authorization': self.headers_str, 'Content-type': 'application/json'}
        self.base_context_name = base_context_name  # название элемента во входном json, содержащего требуемые данные
        self.name = name
        self.json_data = self.get_json()

    def get_json(self) -> dict:
        """Получение данных от YM"""
        json_data = self.get_next_page()
        if "OK" in json_data['status']:
            json_data = self.get_all_pages(json_data=json_data)
        return json_data

    def get_next_page(self, next_page_token=None) -> dict:
        """
        Формирование запроса и получение очередной страницы данных
        (если next_page_token не задан, вернется первая страница)
        """
        url = self.url + f'?page_token={next_page_token}' if next_page_token else self.url
        if self.PARAMS:  # если есть входные параметры, формируем post-запрос
            data = requests.post(url, headers=self.headers, json=self.PARAMS)
        else:
            data = requests.get(url, headers=self.headers)
        return data.json()

    def get_all_pages(self, json_data) -> dict:
        """Получение всех страниц данных"""
        while 'nextPageToken' in json_data['result']['paging']:  # если страница не последняя, читаем следующую
            next_page_token = json_data['result']['paging']['nextPageToken']
            next_json_object = self.get_next_page(next_page_token)
            json_data['result'][self.base_context_name] += next_json_object['result'][self.base_context_name]
            json_data['result']['paging'] = next_json_object['result']['paging']
        return json_data

    def key_error(self) -> str:
        cur_error = int(self.json_data["error"]["code"])
        if cur_error in self.errors:
            return self.errors[cur_error]
        return ''

    def save_with_message(self, request) -> bool:
        try:
            self.save(request)
            messages.success(request, f"Модель {self.name} успешно сохранилась")
            return True
        except KeyError:
            messages.error(request, self.key_error() + f' В моделе {self.name}')
            return False

    def save(self, request) -> None:
        """Сохранение данных в соответствующую БД"""
        raise NotImplementedError


class OfferList(Requests):
    """Класс для получения списка товаров и сохранения в БД Offer"""

    def __init__(self):
        super().__init__(json_name='offer-mapping-entries', base_context_name='offerMappingEntries', name="Offer")

    def save(self, request) -> None:
        OfferPattern(json=self.json_data['result'][self.base_context_name]).save(request.user)


class OfferPrice(Requests):
    """Класс для получения списка цен на товары и сохранения в БД Price"""

    def __init__(self):
        super().__init__(json_name='offer-prices', base_context_name='offers', name="OfferPrice")

    def save(self, request) -> None:
        PricePattern(json=self.json_data['result'][self.base_context_name]).save(request.user)


class OfferChangePrice(Requests):
    """
    Класс для изменения цены на товар на сервере яндекса
    """
    # OfferChangePrice(request, {'656593390': {'price': 1000}})
    def __init__(self, request, data: dict):
        for sku in data.keys():
            data[sku]['old_price'] = self.add_params(sku, data[sku]['price'])
        super().__init__(json_name='offer-prices/updates', base_context_name='price', name='ChangePrices')
        self.update(data, request)
        for sku in sorted(data.keys()):
            self.show(sku, data[sku]['price'], data[sku]['old_price'], data[sku]['new_price'])

    @staticmethod
    def update(data, request) -> None:
        time.sleep(0.4)     # яндекс медленно обновляет данные у себя
        OfferPrice().save(request)  # обновить данные БД
        for sku in data.keys():
            data[sku]['new_price'] = Price.objects.get(
                offer_id=Offer.objects.get(marketSku=sku).id).value

    @staticmethod
    def show(sku, price, old_price, new_price) -> None:
        print(f'marketSku: {sku}, Old price: {old_price}, New price: {new_price}, Status: {"OK" if new_price == price else "ERROR"}')

    def get_json(self) -> dict:
        return self.get_next_page()

    @staticmethod
    def get_dict(offer, price, sku) -> dict:
        return {
            'marketSku': sku,
            'price': {
                        'currencyId': 'RUR',
                        'value': price,
                        'vat': offer.vat,
                    }
            }

    def add_params(self, sku, price) -> int:
        offer_id = Offer.objects.get(marketSku=sku).id
        offer = Price.objects.get(offer_id=offer_id)
        self.PARAMS = {'offers': [self.get_dict(offer, price, sku)]}
        return offer.value  # Вернуть старую цену

