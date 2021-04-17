"""Сериализаторы для OfferReport"""

from rest_framework import serializers
from main.models import *
from main.serializers import BaseListSerializer, BaseModelSerializer, WeightDimensionSerializer


class HidingListSerializer(BaseListSerializer):
    key_fields = ['code']


class HidingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hiding
        fields = ['type', 'code', 'message', 'comment']
        list_serializer_class = HidingListSerializer


class InclusionListSerializer(BaseListSerializer):
    key_fields = ['type']


class InclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inclusion
        fields = ['type', 'count']
        list_serializer_class = InclusionListSerializer


class StorageListSerializer(BaseListSerializer):
    key_fields = ['type']


class StorageSerializer(BaseModelSerializer):
    inclusions = InclusionSerializer(many=True, required=False)

    @staticmethod
    def forward_name():
        return 'storage'

    class Meta:
        model = Storage
        fields = ['type', 'count', 'inclusions']
        list_serializer_class = StorageListSerializer


class TariffListSerializer(BaseListSerializer):
    key_fields = ['type']


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ['type', 'percent', 'amount']
        list_serializer_class = TariffListSerializer


class StockListSerializer(BaseListSerializer):
    key_fields = ['type']


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ['type', 'count', 'offer']
        list_serializer_class = StockListSerializer


class WarehouseReportSerializer(BaseModelSerializer):
    def __init__(self, offer: Offer, **kwargs):
        self.offer = offer
        super().__init__(**kwargs)

    id = serializers.IntegerField(source='warehouse_id', required=False)
    stocks = StockSerializer(many=True, required=False)

    @staticmethod
    def forward_name():
        return 'warehouse'

    def forward_kwargs(self, instance):
        """Словарь для передачи экземпляра модели (instance) дочернему объекту """
        return {'warehouse': instance, 'offer': self.offer}

    def get_nested_object(self, instance, field):
        all_nested_objects = getattr(instance, field, [])
        if all_nested_objects:
            return all_nested_objects.filter(offer=self.offer)
        else:
            return None


    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'stocks']

# class WarehouseReportSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(source='warehouse_id', required=False)
#     stocks = StockSerializer(many=True, required=False)
#
#     def __init__(self, offer: Offer, **kwargs):
#         super().__init__(**kwargs)
#         self.offer = offer
#
#     def forward_kwargs(self, instance):
#         """Словарь для передачи экземпляра модели (instance) дочернему объекту """
#         return {'warehouse': instance, 'offer': self.offer}
#
#     def nested_validated_data(self, instance, data):
#         """validated_data для встроенного сериализатора"""
#         return [{**attrs, **self.forward_kwargs(instance)} for attrs in data]
#
#     def create(self, validated_data):
#         """Создание нового объекта из validated_data"""
#         nested_data: dict = validated_data.pop('stocks', None)
#         instance = Warehouse.objects.create(**validated_data)
#         if nested_data is not None:
#             StockSerializer.create(validated_data=self.nested_validated_data(instance, nested_data))
#         return instance
#
#     def update(self, instance, validated_data):
#         """Обновление объекта instance на основании validated_data"""
#
#         nested_data: dict = validated_data.pop('stocks', None)
#         nested_object = getattr(instance, 'stocks', None)
#         if nested_data is not None:
#             if nested_object is not None:
#                 StockSerializer.update(instance=nested_object,
#                                        validated_data=self.nested_validated_data(instance, nested_data))
#             else:
#                 StockSerializer.create(
#                     validated_data=self.nested_validated_data(instance, nested_data))
#
#         for field, value in validated_data.items():
#             setattr(instance, field, value)
#
#         instance.save()
#
#         return instance
#
#     class Meta:
#         model = Warehouse
#         fields = ['id', 'name', 'stocks']


# class WeightDimensionForReportSerializer(WeightDimensionSerializer):
#     def to_representation(self, instance):
#         return {'weightDimensions': instance.offer.weightDimensions}
#
#     def to_internal_value(self, data: dict):
#         return{
#             'offer.weightDimensions': data
#         }
#
#
class OfferReportSerializer(BaseModelSerializer):
    hidings = HidingSerializer(many=True, required=False)
    storage = StorageSerializer(many=True, required=False)
    tariffs = TariffSerializer(many=True, required=False)

    @staticmethod
    def forward_name():
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
