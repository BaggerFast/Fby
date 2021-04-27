from typing import List
from main.models_addon import Price
from main.models_addon.save_dir import PricePattern
from main.serializers import ChangePriceSerializer
from main.ya_requests.base import Requests


class OfferPrice(Requests):
    """
    Класс для получения списка цен на товары и сохранения в БД Price
    """

    def __init__(self, request):
        super().__init__(json_name='offer-prices', base_context_name='offers', name="OfferPrice", request=request)

    def pattern_save(self) -> None:
        PricePattern(json=self.json_data['result'][self.base_context_name]).save(self.request.user)


class ChangePrices:
    """
    Клас для обработки, проверки и изменения цен
    """
    errors = []
    command = {
        'ya_requests': 'yandex_change',
        'local': 'local_change',
        'update': 'update_DB',
        'check': 'check_prices',
    }

    def __init__(self, keys: List[str], price_list: List = None, request=None):
        """
        Перенаправление на нужные функции по ключу

        ya_requests - отправка данных на YM
        local - изменение данных локально в БД, не затрагивает YM
        update - обновить данные в БД из YM
        check - проверить цены в БД и в price_list
        """
        self.price_list: List = price_list
        self.request = request
        for key in keys:
            getattr(self, self.command[key])()

    def yandex_change(self) -> None:
        """Изменение цен на YM."""
        YandexChangePrices(self.price_list, self.request)

    def local_change(self) -> None:
        """Локальное изменение цен."""
        LocalChangePrices(self.price_list)

    def update_DB(self) -> None:
        """Обновление БД."""
        OfferPrice(self.request).save()

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

        :return: возвращает строку с информацией об изменении цен для вывода в консоль
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

    def __init__(self, price_list: List, request):
        self.temp_params: List = []
        [self.add_params(price) for price in price_list]
        self.PARAMS: dict = {'offers': self.temp_params}
        super().__init__(json_name='offer-prices/updates', base_context_name='price',
                         name='ChangePrices', request=request)

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
