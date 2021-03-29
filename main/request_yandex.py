"""Формирование запросов в YM для получения данных и сохранения их в БД"""

from fby_market.settings import YaMarket
import requests
from main.models import Price
from main.models.save_dir.offer import OfferPattern
from main.models.save_dir.prices import PricePattern


class Requests:
    """
    Базовый класс для получения данных и сохранения в БД
    """

    PARAMS = None  # параметры запроса в формате json (для post-запросов)

    def __init__(self, json_name: str, base_context_name: str):
        self.url = f'https://api.partner.market.yandex.ru/v2/campaigns/{YaMarket.SHOP_ID}/{json_name}.json'
        self.headers_str = f'OAuth oauth_token="{YaMarket.TOKEN}", oauth_client_id="{YaMarket.CLIENT_ID}"'
        self.headers = {'Authorization': self.headers_str, 'Content-type': 'application/json'}
        self.base_context_name = base_context_name  # название элемента во входном json, содержащего требуемые данные
        self.json_data = self.get_json()

    def get_json(self):
        """
        Получение данных от YM
        """
        json_data = self.get_next_page()
        if "OK" in json_data['status']:
            json_data = self.get_all_pages(json_data=json_data)
        return json_data

    def get_next_page(self, next_page_token=None):
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

    def get_all_pages(self, json_data):
        """
        Получение всех страниц данных
        """
        while 'nextPageToken' in json_data['result']['paging']:  # если страница не последняя, читаем следующую
            next_page_token = json_data['result']['paging']['nextPageToken']
            next_json_object = self.get_next_page(next_page_token)
            json_data['result'][self.base_context_name] += next_json_object['result'][self.base_context_name]
            json_data['result']['paging'] = next_json_object['result']['paging']
        return json_data

    def save(self):
        """
        Сохранение данных в соответствующую БД
        """
        raise NotImplementedError


class OfferList(Requests):
    """
    Класс для получения списка товаров и сохранения в БД Offer
    """
    def __init__(self):
        super().__init__(json_name='offer-mapping-entries', base_context_name='offerMappingEntries')

    def save(self):
        OfferPattern(json=self.json_data['result'][self.base_context_name]).save()


class OfferPrice(Requests):
    """
    Класс для получения списка цен на товары и сохранения в БД Price
    """

    def __init__(self):
        super().__init__(json_name='offer-prices', base_context_name='offers')

    def save(self):
        PricePattern(json=self.json_data['result'][self.base_context_name]).save()


class OfferChangePrice(Requests):
    """
    Класс для изменения цены на товар на сервере яндекса
    """
    def __init__(self, data: dict):
        for sku in data.keys():
            data[sku]['old_price'] = self.AddParams(sku, data[sku]['price'])
        super().__init__(json_name='offer-prices/updates', base_context_name='price')
        self.update(data)
        for sku in sorted(data.keys()):
            self.show(sku, data[sku]['price'], data[sku]['old_price'], data[sku]['new_price'])

    @staticmethod
    def update(data) -> None:
        (OfferPrice()).save()  # обновить данные БД
        for sku in data.keys():
            data[sku]['new_price'] = Price.objects.get(marketSku=sku).value

    @staticmethod
    def show(sku, price, old_price, new_price) -> None:
        print(f'marketSku: {sku}, Old price: {old_price}, New price: {new_price}, Status: {"OK" if new_price == price else "ERROR"}')

    def get_json(self) -> dict:
        return self.get_next_page()

    @staticmethod
    def get_dict(offer, price) -> dict:
        return {
            'marketSku': offer.marketSku,
            'price': {
                        'currencyId': 'RUR',
                        'value': price,
                        'vat': offer.vat,
                    }
            }

    def AddParams(self, sku, price) -> int:
        offer = Price.objects.get(marketSku=sku)
        self.PARAMS = {'offers': [self.get_dict(offer, price)]}
        return offer.value  # Вернуть старую цену
