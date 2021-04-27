"""Формирование запросов в YM для получения данных и сохранения их в БД"""
import json
from typing import List
from django.core.exceptions import ObjectDoesNotExist
from main.models_addon import Offer
from main.models_addon.save_dir import *
from main.serializers import OfferSerializer
from main.ya_requests.base import Requests


class OfferList(Requests):
    """
    Класс для получения списка товаров и сохранения в БД Offer
    """

    def __init__(self, request):
        super().__init__(json_name='offer-mapping-entries', base_context_name='offerMappingEntries', name="Offer", request=request)

    def pattern_save(self) -> None:
        OfferPattern(json=self.json_data['result'][self.base_context_name]).save(self.request.user)


class OrderList(Requests):
    """
    Класс для получения списка заказов и сохранения в БД Order
    """

    PARAMS = {  # параметры надо предварительно запросить
        "dateFrom": "2021-01-01",
        "dateTo": "2021-04-17"
    }

    def __init__(self, request, params: dict = None):
        if params is not None:
            self.PARAMS = params
        super().__init__(json_name='/stats/order', base_context_name='order', name="Order", request=request)

    def save(self) -> None:
        OrderPattern(json=self.json_data['result'][self.base_context_name]).save(self.request.user)


class OfferReport(Requests):
    """
    Класс для получения отчета по остаткам товара на складах

    Если задан shop_sku, возвращает отчет по одному товару,
    иначе - по всему списку товаров из каталога
    """

    def __init__(self, request, shop_sku: str = None):
        self.PARAMS = self.get_params() if shop_sku is None else {"shopSkus": [shop_sku]}
        super().__init__(json_name='/stats/skus', base_context_name='shopSkus', name="OfferReport", request=request)

    @staticmethod
    def get_params() -> dict:
        """Возвращает словарь для get-запроса, содержащий список всех всех shopSku из каталога"""
        return {"shopSkus": [offer.shopSku for offer in Offer.objects.all()]}

    def get_json(self) -> dict:
        """Получение данных от YM."""
        return self.get_next_page()

    def save(self) -> None:
        OfferReportPattern(json=self.json_data['result'][self.base_context_name]).save(self.request.user)


class OfferUpdate(Requests):
    """
    Класс для добавления или редактирования товара в YM

    Добавляет товар, указанный в запросе, в ваш каталог товаров и редактирует уже имеющийся товар.
    Чтобы добавить в каталог новый товар, укажите в параметре shop-sku ваш SKU, которого еще нет в каталоге YM.
    Чтобы отредактировать товар из каталога, укажите в параметре shop-sku ваш SKU этого товара в каталоге.
    """

    def __init__(self, request, shop_sku: str):
        self.shop_sku = shop_sku
        self.PARAMS = self.get_params()
        super().__init__(json_name='offer-mapping-entries/updates',
                         base_context_name='offerMappingEntries',
                         name="OfferUpdate",
                         request=request
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
        offer_data = json.loads(json.dumps(offer_serializer.data, ensure_ascii=False))
        offer_data = {key: value for key, value in offer_data.items() if value and key != 'processingState'}

        offer_mapping_entry = {'offer': offer_data}
        print(offer_mapping_entry)

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

    def __init__(self, offers: List[Offer], request):
        self.request = request
        self.offers: List[Offer] = offers
        self.errors: dict = dict()
        self.success: dict = dict()

    def update_offers(self) -> None:
        """Обновляет или добавляет товары из списка self.offers."""
        for offer in self.offers:
            sku = offer.shopSku
            answer = OfferUpdate(sku, self.request).get_answer()
            if answer['status'] == 'ERROR':
                self.errors[sku] = self.get_error_messages(answer)
            elif answer['status'] == 'OK':
                self.success[sku] = 'OK'

    def get_error_messages(self, answer: dict) -> List[str]:
        """Формирует список сообщений об ошибках"""
        error_messages = []
        for item in answer['errors']:
            if item['code'] in self.ERRORS:
                item['code'] = f'{item["code"]} ({self.ERRORS[item["code"]]})'
            error_messages.append(f'{item["code"]}: {item["message"]}')
        return error_messages
