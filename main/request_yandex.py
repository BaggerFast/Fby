"""Формирование запросов в YM для получения данных и сохранения их в БД"""

from fby_market.settings import YaMarket
import requests
from main.models.save_dir.offer import OfferPattern
from main.models.save_dir.prices import PricePattern


class Requests:
    """Базовый класс для получения данных и сохранения в БД"""

    PARAMS = None  # параметры запроса в формате json (для post-запросов)

    def __init__(self, json_name: str, base_context_name: str):
        self.url = f'https://api.partner.market.yandex.ru/v2/campaigns/{YaMarket.SHOP_ID}/{json_name}.json'
        self.headers_str = f'OAuth oauth_token="{YaMarket.TOKEN}", oauth_client_id="{YaMarket.CLIENT_ID}"'
        self.headers = {'Authorization': self.headers_str, 'Content-type': 'application/json'}
        self.base_context_name = base_context_name  # название элемента во входном json, содержащего требуемые данные
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
        if int(self.json_data["error"]["code"]) == 420:
            return f'Ошибка № {420}. Превышенно кол-во запросов в сутки. Попробуйте позже'
        return ''

    def save_with_message(self) -> str:
        try:
            self.save()
        except KeyError:
            return self.key_error()
        return ""

    def save(self) -> None:
        """Сохранение данных в соответствующую БД"""
        raise NotImplementedError


class OfferList(Requests):
    """Класс для получения списка товаров и сохранения в БД Offer"""

    def __init__(self, user):
        super().__init__(json_name='offer-mapping-entries', base_context_name='offerMappingEntries')
        self.user = user

    def save(self) -> None:
        OfferPattern(json=self.json_data['result'][self.base_context_name]).save(self.user)


class OfferPrice(Requests):
    """Класс для получения списка цен на товары и сохранения в БД Price"""

    def __init__(self, user):
        super().__init__(json_name='offer-prices', base_context_name='offers')
        self.user = user

    def save(self) -> None:
        PricePattern(json=self.json_data['result'][self.base_context_name]).save(self.user)
