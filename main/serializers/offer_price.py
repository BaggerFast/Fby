"""Сериализаторы всея моделей"""

from rest_framework import serializers
from rest_framework.serializers import ListSerializer
from main.models import *


class PriceSerializer(serializers.ModelSerializer):
    def get_data(self) -> dict:
        return {**self.data, 'currencyId': 'RUR'}

    class Meta:
        model = Price
        exclude = ('offer', 'id', 'vat', 'discountBase')  # исключая offer


class WeightDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightDimension
        exclude = ('offer', 'id',)  # исключая offer


class TimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timing
        fields = ['timePeriod', 'timeUnit', 'comment']


class ProcessingStateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingStateNote
        exclude = ('processingState', 'id')


class ProcessingStateSerializer(serializers.ModelSerializer):
    notes = ProcessingStateNoteSerializer()

    class Meta:
        model = ProcessingState
        fields = ['status', 'notes']


class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mapping
        exclude = ('offer', 'mappingType', 'id')


class OfferSerializer(serializers.ModelSerializer):
    price = PriceSerializer()
    weightDimensions = WeightDimensionSerializer()
    manufacturerCountries = ListSerializer(child=serializers.CharField())
    urls = ListSerializer(child=serializers.CharField())
    barcodes = ListSerializer(child=serializers.CharField())
    shelfLife = TimingSerializer()
    lifeTime = TimingSerializer()
    guaranteePeriod = TimingSerializer()
    customsCommodityCodes = ListSerializer(child=serializers.CharField())
    supplyScheduleDays = ListSerializer(child=serializers.CharField())
    processingState = ProcessingStateSerializer()
    mapping = MappingSerializer()
    awaitingModerationMapping = MappingSerializer()
    rejectedMapping = MappingSerializer()

    class Meta:
        model = Offer
        fields = [
            'marketSku',
            'updatedAt',
            'shopSku',
            'name',
            'category',
            'manufacturer',
            'price',
            'weightDimensions',
            'manufacturerCountries',
            'urls',
            'barcodes',
            'description',
            'shelfLife',
            'lifeTime',
            'guaranteePeriod',
            'customsCommodityCodes',
            'certificate',
            'availability',
            'transportUnitSize',
            'minShipment',
            'quantumOfSupply',
            'supplyScheduleDays',
            'deliveryDurationDays',
            'boxCount',
            'shelfLifeDays',
            'lifeTimeDays',
            'guaranteePeriodDays',
            'processingState',
            'mapping',
            'awaitingModerationMapping',
            'rejectedMapping'
        ]
