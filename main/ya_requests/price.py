from typing import List
from django.http import HttpRequest
from django.contrib import messages
from main.models_addon.ya_market import Price
from main.models_addon.save_dir import PricePattern
from main.serializers import ChangePriceSerializer
from main.ya_requests.base import Requests


class OfferPrice(Requests):
    """
    Класс для получения списка цен на товары и сохранения в БД Price
    """

    def __init__(self, request: HttpRequest):
        super().__init__(json_name='offer-prices', base_context_name='offers', name="OfferPrice", request=request)

    def pattern_save(self) -> None:
        PricePattern(json=self.json_data['result'][self.base_context_name]).save(self.request.user)


class ChangePrices:
    """
    Клас для обработки, проверки и изменения цен
    """
    errors = []

    def check_prices(self) -> None:
        """Проверка цен в БД и price_list."""
        for price in self.price_list:
            db_price = Price.objects.get(offer=price.offer)
            if db_price.value != price.value:
                self.errors.append(price)

    def __init__(self, keys: List[str], price_list: List = None, request: HttpRequest = None):
        self.command = {
            'ya_requests': lambda: YandexChangePrices(self.price_list, self.request).update_prices(),
            'local': lambda: LocalChangePrices(price_list),
            'update': lambda: OfferPrice(self.request).save(),
            'check': self.check_prices,
        }

        """
        Перенаправление на нужные функции по ключу
        ya_requests - отправка данных на YM
        local - изменение данных локально в БД, не затрагивает YM
        update - обновить данные в БД из YM
        check - проверить цены в БД и в price_list
        """

        self.price_list: List = price_list
        self.request: HttpRequest = request

        for key in keys:
            if key in keys:
                self.command[key]()


def sku_and_price(price):
    return {'shopSku': price.offer.shopSku, 'price': ChangePriceSerializer(price).data}


class LocalChangePrices:
    """
    Класс для изменения цены только в БД
    """

    def __init__(self, price_list: List):
        data: List = [self.change_price(price) for price in price_list]

    @staticmethod
    def change_price(price) -> dict:
        """
        Изменить цену локально в БД

        :return: возвращает строку с информацией об изменении цен для вывода в консоль
        """
        price_object = Price.objects.get(offer=price.offer)
        price_object.value = price.value
        price_object.save()
        return sku_and_price(price_object)


class YandexChangePrices(Requests):
    """
    Класс для изменения цены на товар на сервере YM
    """
    def __init__(self, price: Price, request: HttpRequest):
        self.price_list: Price = price
        self.temp_params: List = [sku_and_price(price)] if price.value else []
        self.errors = {}
        self.params: dict = {'offers': self.temp_params}
        super().__init__(json_name='offer-prices/updates', base_context_name='price', name='ChangePrices',
                         request=request)

    def get_answer(self) -> dict:
        """Возвращает ответ от YM

        OK — запрос выполнен успешно, все товары отправлены на модерацию.
        ERROR — хотя бы в одном товаре найдена ошибка, и ни один товар не отправлен на модерацию.
        Если ERROR, далее следует список ошибок
        """
        return self.json_data

    def get_json(self) -> dict:
        """Получение данных от YM."""
        return self.get_next_page()


class YandexChangePricesList:
    ERRORS = {
        'DUPLICATE_OFFER': 'В теле запроса передано два или более товара '
                           'с одинаковыми значениями параметров market-sku',
        'LIMIT_EXCEEDED': 'Превышено индивидуальное ограничение на количество передаваемых товаров',
        'REQUEST_LIMIT_EXCEEDED': 'В теле запроса в параметре offers передано больше 2000 товаров'
    }

    def __init__(self, prices: List[Price], request: HttpRequest):
        self.request: HttpRequest = request
        self.prices: List[Price] = prices
        self.errors: dict = dict()

    def update_prices(self) -> None:
        """Обновляет или добавляет товары из списка self.offers."""
        for price in self.prices:
            sku = price.offer.shopSku
            answer = YandexChangePrices(request=self.request, price=price).get_answer()
            if answer['status'] == 'ERROR':
                self.errors[sku] = self.get_error_messages(answer)
            elif answer['status'] == 'OK':
                price.has_changed = False
                price.save(update_fields=['has_changed'])

    def get_error_messages(self, answer: dict) -> List[str]:
        """Формирует список сообщений об ошибках"""
        error_messages = []
        for item in answer['errors']:
            if item['code'] in self.ERRORS:
                item['code'] = self.ERRORS[item["code"]]
            error_messages.append(f' {item["code"]}: {item["message"]}')
        return error_messages

    def messages(self, sku_list: list, success_message: str):
        if not self.errors:
            messages.success(self.request, success_message)
            return
        for sku in sku_list:
            if sku in self.errors:
                errors = f'Ошибка при сохранении цены товара shopSku = {sku} на Яндексе.'
                errors += ' '.join(self.errors[sku])
                messages.error(self.request, errors)
