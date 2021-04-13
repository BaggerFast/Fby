"""Формирование запросов в YM для получения данных и сохранения их в БД"""
import json

from django.contrib import messages
from fby_market.settings import YaMarket
import requests

from main.models import Price
from main.models.save_dir import *
from main.serializers import PriceSerializer


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

    def save(self, request) -> bool:
        """
        возвращает True, когда модель успешно сохранилась,
        иначе False
        """
        try:
            self.pattern_save(request)
            messages.success(request, f"Модель {self.name} успешно сохранилась")
            return True
        except KeyError:
            messages.error(request, self.key_error() + f' В модели {self.name}')
            return False

    def pattern_save(self, request) -> None:
        """Сохранение данных в соответствующую БД, используется при GET запрос"""
        pass

    def save_json_to_file(self, file):
        with open(file, "w") as write_file:
            json.dump(self.json_data, write_file, indent=2, ensure_ascii=False)


class OfferList(Requests):
    """Класс для получения списка товаров и сохранения в БД Offer"""

    def __init__(self):
        super().__init__(json_name='offer-mapping-entries', base_context_name='offerMappingEntries', name="Offer")

    def pattern_save(self, request) -> None:
        OfferPattern(json=self.json_data['result'][self.base_context_name]).save(request.user)


class OfferPrice(Requests):
    """Класс для получения списка цен на товары и сохранения в БД Price"""

    def __init__(self):
        super().__init__(json_name='offer-prices', base_context_name='offers', name="OfferPrice")

    def pattern_save(self, request) -> None:
        PricePattern(json=self.json_data['result'][self.base_context_name]).save(request.user)


class ChangePrices:
    """
    Клас для обработки, проверки и изменения цен
    """
    errors = []
    command = {
        'yandex': 'yandex_change',
        'local': 'local_change',
        'update': 'update_DB',
        'check': 'check_prices',
    }

    def __init__(self, key, price_list: list = None, request=None):
        """
        Перепанравление на нужные функции по ключу

        yandex - отправка данных на YM
        local - изменение данных локально в БД, не затрагивает YM
        update - обновить данные в БД из YM
        check - проверить цены в БД и в price_list
        """
        self.price_list = price_list
        self.request = request
        getattr(self, self.command[key])()

    def yandex_change(self):
        """
        Изменение цен на YM
        """
        YandexChangePrices(self.price_list)

    def local_change(self):
        """
        Локальное изменение цен
        """
        LocalChangePrices(self.price_list)

    def update_data_base(self):
        """
        Обновление БД
        """
        OfferPrice().save(self.request)

    def check_prices(self):
        """
        Проверка цен в БД и price_list
        """
        for price in self.price_list:
            db_price = Price.objects.get(offer=price.offer)
            if db_price.value != price.value:
                print(f'sku: {db_price.offer.shopSku}, db price: {db_price.value},'
                      f'list price: {price.value}')
                self.errors.append(price)


class LocalChangePrices:
    """
    Класс для изменения цены только в БД
    """

    def __init__(self, price_list: list):
        data = [self.change_price(price) for price in price_list]
        self.show(data)

    @staticmethod
    def show(data):
        """
        Вывод данных об изменении цен
        """
        print(*data)

    @staticmethod
    def change_price(price) -> dict:
        """
        Изменить цену локально в БД

        :return: возвращает строку с ифнормацией об изменении цен для вывода в консоль
        """
        price_object = Price.objects.get(offer=price.offer)
        price_object.value = price.value
        price_object.save()
        return {'shopSku': price_object.offer.shopSku,
                'price': PriceSerializer(price_object).get_data()}


class YandexChangePrices(Requests):
    """
    Класс для изменения цены на товар на сервере YM
    """

    def __init__(self, price_list: list):
        self.temp_params = []
        [self.add_params(price) for price in price_list]
        self.PARAMS = {'offers': self.temp_params}
        super().__init__(json_name='offer-prices/updates', base_context_name='price',
                         name='ChangePrices')

    @staticmethod
    def get_dict(price) -> dict:
        """
        Получить словарь, отправляемый для изменения цен на YM
        """
        return {'shopSku': price.offer.shopSku, 'price': PriceSerializer(price).get_data()}

    def get_json(self) -> dict:
        """
        Получение данных от YM
        """
        return self.get_next_page()

    def add_params(self, price) -> None:
        """
        Добавить в PARAMS запрос на одну цену
        """
        if price.value:
            self.temp_params += [self.get_dict(price)]


class OrderList(Requests):
    """Класс для получения списка заказов и сохранения в БД Order"""

    PARAMS = {                      # параметры надо предварительно запросить
        "dateFrom": "2021-01-01",
        "dateTo": "2021-04-04"
    }

    def __init__(self, params: dict = None):
        super().__init__(json_name='/stats/orders', base_context_name='orders', name="Order")
        if params is not None:
            self.PARAMS = params

    def save(self, request=None) -> None:
        OrderPattern(json=self.json_data['result'][self.base_context_name]).save(request.user)
