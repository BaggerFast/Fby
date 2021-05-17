"""Сериализаторы для модели OfferReport"""

from typing import List
from rest_framework import serializers
from main.models_addon.ya_market import Hiding, Inclusion, Storage, Tariff, Stock, Offer, Warehouse, OfferReport
from main.serializers import BaseListSerializer, BaseModelSerializer, SimpleModelSerializer


class HidingListSerializer(BaseListSerializer):
    """Сериализатор списков для модели Hiding"""
    key_fields = ['code']


class HidingSerializer(SimpleModelSerializer):
    """Сериализатор для модели Hiding"""

    class Meta:
        model = Hiding
        fields = ['type', 'code', 'message', 'comment']
        list_serializer_class = HidingListSerializer


class InclusionListSerializer(BaseListSerializer):
    """Сериализатор списков для модели Inclusion"""
    key_fields = ['type']


class InclusionSerializer(SimpleModelSerializer):
    """Сериализатор для модели Inclusion"""

    class Meta:
        model = Inclusion
        fields = ['type', 'count']
        list_serializer_class = InclusionListSerializer


class StorageListSerializer(BaseListSerializer):
    """Сериализатор списков для модели Storage"""
    key_fields = ['type']


class StorageSerializer(BaseModelSerializer):
    """Сериализатор для модели Storage"""
    inclusions = InclusionSerializer(many=True, required=False)

    @staticmethod
    def forward_name():
        """Ключ для передачи вложенным моделям"""
        return 'storage'

    class Meta:
        model = Storage
        fields = ['type', 'count', 'inclusions']
        list_serializer_class = StorageListSerializer


class TariffListSerializer(BaseListSerializer):
    """Сериализатор списков для модели Tariff"""
    key_fields = ['type']


class TariffSerializer(SimpleModelSerializer):
    """Сериализатор для модели Tariff"""

    class Meta:
        model = Tariff
        fields = ['type', 'percent', 'amount']
        list_serializer_class = TariffListSerializer


class StockListSerializer(BaseListSerializer):
    """Сериализатор списков для модели Stock"""
    key_fields = ['type']


class StockSerializer(SimpleModelSerializer):
    """Сериализатор для модели Stock"""

    class Meta:
        model = Stock
        fields = ['type', 'count', 'offer']
        list_serializer_class = StockListSerializer


class WarehouseReportSerializer(BaseModelSerializer):
    """Сериализатор для модели Warehouse (вложенный, для сериализатора OfferReport)"""

    def __init__(self, offer: Offer, **kwargs: dict):
        self.offer = offer  # объект передается вложенному сериализатору Stock
        super().__init__(**kwargs)

    id = serializers.IntegerField(source='warehouse_id', required=False)
    stocks = StockSerializer(many=True, required=False)

    @staticmethod
    def forward_name():
        """Ключ для передачи вложенным моделям"""
        return 'warehouse'

    def forward_kwargs(self, instance) -> dict:
        """Словарь для передачи экземпляра модели (instance) вложенному объекту """
        return {'warehouse': instance, 'offer': self.offer}

    def get_nested_object(self, instance, field: str) -> List:
        """Возвращает список вложенных объектов, дополнительно отфильтрованный по полю offer """
        all_nested_objects = getattr(instance, field, [])
        if all_nested_objects:
            return all_nested_objects.filter(offer=self.offer)
        else:
            return []

    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'stocks']


class OfferReportSerializer(BaseModelSerializer):
    """Сериализатор для модели OfferReport"""
    hidings = HidingSerializer(many=True, required=False)
    storage = StorageSerializer(many=True, required=False)
    tariffs = TariffSerializer(many=True, required=False)

    @staticmethod
    def forward_name():
        """Ключ для передачи вложенным моделям"""
        return 'report'

    class Meta:
        model = OfferReport
        fields = ['shopSku',
                  'marketSku',
                  'name',
                  'price',
                  'categoryId',
                  'categoryName',
                  'hidings',
                  'storage',
                  'tariffs'
                  ]
