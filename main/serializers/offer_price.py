"""Сериализаторы всея моделей"""

from rest_framework import serializers
from main.models import *
from main.serializers import BaseListSerializer, BaseModelSerializer


class ChangePriceSerializer(serializers.ModelSerializer):
    def get_data(self) -> dict:
        return {**self.data, 'currencyId': 'RUR'}

    class Meta:
        model = Price
        fields = ['value']


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ['currencyId', 'discountBase', 'value', 'vat']


class OfferForPriceSerializer(BaseModelSerializer):
    price = PriceSerializer()

    @staticmethod
    def forward_name():
        return 'offer'

    class Meta:
        model = Offer
        fields = ['price', 'shopSku', 'marketSku', 'updatedAt']


class WeightDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightDimension
        exclude = ('offer', 'id',)  # исключая offer


class ShelfLifeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelfLife
        fields = ['timePeriod', 'timeUnit', 'comment']


class LifeTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeTime
        fields = ['timePeriod', 'timeUnit', 'comment']


class GuaranteePeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuaranteePeriod
        fields = ['timePeriod', 'timeUnit', 'comment']


class ProcessingStateNoteListSerializer(BaseListSerializer):
    key_fields = ['type']


class ProcessingStateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingStateNote
        exclude = ('processingState', 'id')
        list_serializer_class = ProcessingStateNoteListSerializer


class ProcessingStateSerializer(BaseModelSerializer):
    notes = ProcessingStateNoteSerializer(many=True, required=False)

    @staticmethod
    def forward_name():
        return 'processingState'

    class Meta:
        model = ProcessingState
        fields = ['status', 'notes']


class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mapping
        exclude = ('offer', 'mappingType', 'id')


class ManufacturerCountryListSerializer(BaseListSerializer):
    key_fields = ['name']


class ManufacturerCountrySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.name

    def to_internal_value(self, data):
        return{'name': data}

    class Meta:
        model = ManufacturerCountry
        fields = ['name']
        list_serializer_class = ManufacturerCountryListSerializer


class UrlListSerializer(BaseListSerializer):
    key_fields = ['url']


class UrlSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.url

    def to_internal_value(self, data):
        return{'url': data}

    class Meta:
        model = Url
        fields = ['url']
        list_serializer_class = UrlListSerializer


class BarcodeListSerializer(BaseListSerializer):
    key_fields = ['barcode']


class BarcodeSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.barcode

    def to_internal_value(self, data):
        return{'barcode': data}

    class Meta:
        model = Barcode
        fields = ['barcode']
        list_serializer_class = BarcodeListSerializer


class CustomsCommodityCodeListSerializer(BaseListSerializer):
    key_fields = ['code']


class CustomsCommodityCodeSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.code

    def to_internal_value(self, data):
        return{'code': data}

    class Meta:
        model = CustomsCommodityCode
        fields = ['code']
        list_serializer_class = CustomsCommodityCodeListSerializer


class SupplyScheduleDaysListSerializer(BaseListSerializer):
    key_fields = ['supplyScheduleDay']


class SupplyScheduleDaysSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.supplyScheduleDay

    def to_internal_value(self, data):
        return{'supplyScheduleDay': data}

    class Meta:
        model = SupplyScheduleDays
        fields = ['supplyScheduleDay']
        list_serializer_class = SupplyScheduleDaysListSerializer


class OfferSerializer(BaseModelSerializer):
    weightDimensions = WeightDimensionSerializer(required=False)
    manufacturerCountries = ManufacturerCountrySerializer(many=True, required=False)
    urls = UrlSerializer(many=True, required=False)
    barcodes = BarcodeSerializer(many=True, required=False)
    shelfLife = ShelfLifeSerializer(required=False)
    lifeTime = LifeTimeSerializer(required=False)
    guaranteePeriod = GuaranteePeriodSerializer(required=False)
    customsCommodityCodes = CustomsCommodityCodeSerializer(many=True, required=False)
    supplyScheduleDays = SupplyScheduleDaysSerializer(many=True, required=False)
    processingState = ProcessingStateSerializer(required=False)

    @staticmethod
    def forward_name():
        return 'offer'

    class Meta:
        model = Offer
        fields = [
            'shopSku',
            'name',
            'vendor',
            'vendorCode',
            'category',
            'manufacturer',
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
        ]
