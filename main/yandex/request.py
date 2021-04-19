"""Формирование запросов в YM для получения данных и сохранения их в БД"""

from typing import List
import json
from django.contrib import messages
from fby_market.settings import YaMarket
import requests
from django.core.exceptions import ObjectDoesNotExist

from main.models_addon import Price, Offer
from main.models_addon.save_dir import *
from main.serializers import PriceSerializer, OfferSerializer


class Requests:
    """
    Базовый класс для получения данных и сохранения в БД
    """

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
        self.url: str = f'https://api.partner.market.yandex.ru/v2/campaigns/{YaMarket.SHOP_ID}/{json_name}.json'
        self.headers_str: str = f'OAuth oauth_token="{YaMarket.TOKEN}", oauth_client_id="{YaMarket.CLIENT_ID}"'
        self.headers: dict = {'Authorization': self.headers_str, 'Content-type': 'application/json'}
        self.base_context_name: str = base_context_name  # название элемента во входном json, содержащего требуемые данные
        self.name: str = name
        self.json_data: dict = self.get_json()

    def get_json(self) -> dict:
        """Получение данных от YM"""
        json_data = self.get_next_page()
        if "OK" in json_data['status']:
            json_data = self.get_all_pages(json_data=json_data)
        return json_data

    def get_next_page(self, next_page_token: str = None) -> dict:
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

    def get_all_pages(self, json_data: dict) -> dict:
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
        """Возвращает True, когда модель успешно сохранилась, иначе False"""
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

    def save_json_to_file(self, file: str) -> None:
        """Сохранение данных в json-файл"""
        with open(file, "w") as write_file:
            json.dump(self.json_data, write_file, indent=2, ensure_ascii=False)


class OfferList(Requests):
    """
    Класс для получения списка товаров и сохранения в БД Offer
    """

    def __init__(self):
        super().__init__(json_name='offer-mapping-entries', base_context_name='offerMappingEntries', name="Offer")

    def pattern_save(self, request) -> None:
        OfferPattern(json=self.json_data['result'][self.base_context_name]).save(request.user)


class OfferPrice(Requests):
    """
    Класс для получения списка цен на товары и сохранения в БД Price
    """

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

    def __init__(self, key: str, price_list: List = None, request=None):
        """
        Перепнаравление на нужные функции по ключу

        yandex - отправка данных на YM
        local - изменение данных локально в БД, не затрагивает YM
        update - обновить данные в БД из YM
        check - проверить цены в БД и в price_list
        """
        self.price_list: List = price_list
        self.request = request
        getattr(self, self.command[key])()

    def yandex_change(self) -> None:
        """Изменение цен на YM."""
        YandexChangePrices(self.price_list)

    def local_change(self) -> None:
        """Локальное изменение цен."""
        LocalChangePrices(self.price_list)

    def update_data_base(self) -> None:
        """Обновление БД."""
        OfferPrice().save(self.request)

    def check_prices(self) -> None:
        """Проверка цен в БД и price_list."""
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

    def __init__(self, price_list: List):
        data: List = [self.change_price(price) for price in price_list]
        self.show(data)

    @staticmethod
    def show(data):
        """Вывод данных об изменении цен."""
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
                'price': ChangePriceSerializer(price_object).get_data()}


class YandexChangePrices(Requests):
    """
    Класс для изменения цены на товар на сервере YM
    """

    def __init__(self, price_list: List):
        self.temp_params: List = []
        [self.add_params(price) for price in price_list]
        self.PARAMS: dict = {'offers': self.temp_params}
        super().__init__(json_name='offer-prices/updates', base_context_name='price',
                         name='ChangePrices')

    @staticmethod
    def get_dict(price) -> dict:
        """Получить словарь, отправляемый для изменения цен на YM."""
        return {'shopSku': price.offer.shopSku, 'price': ChangePriceSerializer(price).get_data()}

    def get_json(self) -> dict:
        """Получение данных от YM."""
        return self.get_next_page()

    def add_params(self, price) -> None:
        """Добавить в PARAMS запрос на одну цену."""
        if price.value:
            self.temp_params += [self.get_dict(price)]


class OrderList(Requests):
    """
    Класс для получения списка заказов и сохранения в БД Order
    """

    PARAMS = {  # параметры надо предварительно запросить
        "dateFrom": "2021-01-01",
        "dateTo": "2021-04-17"
    }

    def __init__(self, params: dict = None):
        if params is not None:
            self.PARAMS = params
        super().__init__(json_name='/stats/orders', base_context_name='orders', name="Order")

    def save(self, request) -> None:
        OrderPattern(json=self.json_data['result'][self.base_context_name]).save(request.user)


class OfferReport(Requests):
    """
    Класс для получения отчета по остаткам товара на складах

    Если задан shop_sku, возвращает отчет по одному товару,
    иначе - по всему списку товаров из каталога
    """

    def __init__(self, shop_sku: str = None):
        self.PARAMS = self.get_params() if shop_sku is None else {"shopSkus": [shop_sku]}
        super().__init__(json_name='/stats/skus', base_context_name='shopSkus', name="OfferReport")

    @staticmethod
    def get_params() -> dict:
        """Возвращает словарь для get-запроса, содержащий список всех всех shopSku из каталога"""
        return {"shopSkus": [offer.shopSku for offer in Offer.objects.all()]}

    def get_json(self) -> dict:
        """Получение данных от YM."""
        return self.get_next_page()

    def save(self, request) -> None:
        OfferReportPattern(json=self.json_data['result'][self.base_context_name]).save(request.user)


class OfferUpdate(Requests):
    """
    Класс для добавления или редактирования товара в YM

    Добавляет товар, указанный в запросе, в ваш каталог товаров и редактирует уже имеющийся товар.
    Чтобы добавить в каталог новый товар, укажите в параметре shop-sku ваш SKU, которого еще нет в каталоге YM.
    Чтобы отредактировать товар из каталога, укажите в параметре shop-sku ваш SKU этого товара в каталоге.
    """

    def __init__(self, shop_sku: str):
        self.shop_sku = shop_sku
        self.PARAMS = self.get_params()
        super().__init__(json_name='offer-mapping-entries/updates',
                         base_context_name='offerMappingEntries',
                         name="OfferUpdate"
                         )

    def get_params(self) -> dict:
        """Возвращает словарь для get-запроса, содержащий информацию о товаре"""
        try:
            offer = Offer.objects.get(shopSku=self.shop_sku)
        except ObjectDoesNotExist:
            print('Товара с таким shopSku нет в каталоге')
            return dict()

        offer_mapping_entry = self.get_offer_mapping_entry(offer)
        offer_mapping_entries = {'offerMappingEntries': [offer_mapping_entry]}

        return offer_mapping_entries

    @staticmethod
    def get_offer_mapping_entry(offer: Offer) -> dict:
        """Возвращает элемент словаря для товара offer"""
        offer_serializer = OfferSerializer(offer)
        offer_data = offer_serializer.data
        offer_data = {key: value for key, value in offer_data.items() if value and key != 'processingState'}

        offer_mapping_entry = {'offer': offer_data}

        offer_mapping = offer.mapping_set.filter(mappingType='BASE').first()
        if offer_mapping:
            offer_market_sku = getattr(offer_mapping, 'marketSku', None)
            if offer_market_sku:
                mapping_data = {'marketSku': offer_market_sku}
                offer_mapping_entry['mapping'] = mapping_data

        return offer_mapping_entry

    def get_json(self) -> dict:
        """Отправка данных и получение ответа от YM."""
        return self.get_next_page()

    def get_answer(self) -> dict:
        """Возвращает ответ от YM

        OK — запрос выполнен успешно, все товары отправлены на модерацию.
        ERROR — хотя бы в одном товаре найдена ошибка, и ни один товар не отправлен на модерацию.
        Если ERROR, далее следует список ошибок
        """
        return self.json_data


class UpdateOfferList:
    """
    Класс для добавления или редактирования списка товара в YM

    :param offers: товары для добавления/редактирования (список)
    :param errors: сообщения об ошибках (список словарей вида: {shopSku: список ошибок})
    :param success: сообщения об успехах (список словарей вида: {shopSku: 'OK'})
    """
    ERRORS = {
        'BAD_REQUEST': 'у вас нет доступа к добавлению товаров в каталог'
                       'Убедитесь, что отправляете корректный запрос',
        'CONSTRAINT_VIOLATION': 'у товара не указаны значения параметров manufacturer-countries '
                                'и/или url',
        'DUPLICATE_OFFER': 'в запросе передан другой товар с тем же значением параметра shop-sku',
        'INVALID_MARKET_SKU': 'у товара указано несуществующее значение параметра market-sku',
        'INVALID_OFFER_ID': 'у товара длина значения параметра shop-sku превышает 80 символов '
                            'и/или оно содержит символы, которые отличаются от печатных символов '
                            'из таблицы ASCII',
        'INVALID_SHOP_SKU': 'у товара указано некорректное значение параметра shop-sku',
        'MISSING_OFFER': 'у товара нет параметра offer',
        'NO_REQUIRED_FIELDS': 'у товара нет обязательных параметров',
        'PROBLEMS_IN_OTHER_OFFERS': 'информация о товаре корректна, но не отправлена на модерацию '
                                    'из‑за ошибок в других товарах'
    }

    def __init__(self, offers: List[Offer]):
        self.offers: List[Offer] = offers
        self.errors: List[dict] = []
        self.success: List[dict] = []

    def update_offers(self) -> None:
        """Обновляет или добавляет товары из списка self.offers."""
        for offer in self.offers:
            sku = offer.shopSku
            answer = OfferUpdate(sku).get_answer()
            if answer['status'] == 'ERROR':
                self.errors.append({sku: self.get_error_messages(answer)})
            elif answer['status'] == 'OK':
                self.success.append({sku: 'OK'})

    def get_error_messages(self, answer: dict) -> List[str]:
        """Формирует список сообщений об ошибках"""
        error_messages = []
        for item in answer['errors']:
            if item['code'] in self.ERRORS:
                item['code'] = f'{item["code"]} ({self.ERRORS[item["code"]]})'
            error_messages.append(f'{item["code"]}: {item["message"]}')
        return error_messages
