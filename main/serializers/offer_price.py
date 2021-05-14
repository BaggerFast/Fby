"""Сериализаторы для модели Offer"""

from rest_framework import serializers
from main.models_addon import *
from main.serializers import BaseListSerializer, BaseModelSerializer, SimpleModelSerializer


class ChangePriceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Price (для изменения цены)"""
    def get_data(self) -> dict:
        return {**self.data, 'currencyId': 'RUR'}

    class Meta:
        model = Price
        fields = ['value']


class PriceSerializer(SimpleModelSerializer):
    """Сериализатор для модели Price (встроенный, для сериализации OfferForPrice)"""

    class Meta:
        model = Price
        fields = ['currencyId', 'discountBase', 'value', 'vat']


class OfferForPriceSerializer(BaseModelSerializer):
    """Сериализатор для модели Offer (встроенный, для сериализации Price)"""
    price = PriceSerializer()

    @staticmethod
    def forward_name():
        """Ключ для передачи вложенным моделям"""
        return 'offer'

    class Meta:
        model = Offer
        fields = ['price', 'shopSku', 'marketSku', 'updatedAt']


class WeightDimensionSerializer(SimpleModelSerializer):
    """Сериализатор для модели WeightDimension"""
    class Meta:
        model = WeightDimension
        fields = ['length', 'width', 'height', 'weight']


class ShelfLifeSerializer(SimpleModelSerializer):
    """Сериализатор для модели ShelfLife"""
    class Meta:
        model = ShelfLife
        fields = ['timePeriod', 'timeUnit', 'comment']


class LifeTimeSerializer(SimpleModelSerializer):
    """Сериализатор для модели LifeTime"""
    class Meta:
        model = LifeTime
        fields = ['timePeriod', 'timeUnit', 'comment']


class GuaranteePeriodSerializer(SimpleModelSerializer):
    """Сериализатор для модели GuaranteePeriod"""
    class Meta:
        model = GuaranteePeriod
        fields = ['timePeriod', 'timeUnit', 'comment']


class ProcessingStateNoteListSerializer(BaseListSerializer):
    """Сериализатор списков для модели ProcessingStateNote"""
    key_fields = ['type']


class ProcessingStateNoteSerializer(SimpleModelSerializer):
    """Сериализатор для модели ProcessingStateNote"""
    class Meta:
        model = ProcessingStateNote
        fields = ['type', 'payload']
        list_serializer_class = ProcessingStateNoteListSerializer


class ProcessingStateSerializer(BaseModelSerializer):
    """Сериализатор для модели ProcessingState"""
    notes = ProcessingStateNoteSerializer(many=True, required=False)

    @staticmethod
    def forward_name():
        """Ключ для передачи вложенным моделям"""
        return 'processingState'

    class Meta:
        model = ProcessingState
        fields = ['status', 'notes']


class MappingSerializer(SimpleModelSerializer):
    """Сериализатор для модели Mapping"""
    class Meta:
        model = Mapping
        fields = ['marketSku', 'modelId', 'categoryId']


class ManufacturerCountryListSerializer(BaseListSerializer):
    """Сериализатор списков для модели ManufacturerCountry"""
    key_fields = ['name']


class ManufacturerCountrySerializer(SimpleModelSerializer):
    """Сериализатор для модели ManufacturerCountry"""
    def to_representation(self, instance):
        return instance.name

    def to_internal_value(self, data):
        return{'name': data}

    class Meta:
        model = ManufacturerCountry
        fields = ['name']
        list_serializer_class = ManufacturerCountryListSerializer


class UrlListSerializer(BaseListSerializer):
    """Сериализатор списков для модели Url"""
    key_fields = ['url']


class UrlSerializer(SimpleModelSerializer):
    """Сериализатор для модели Url"""
    def to_representation(self, instance):
        return instance.url

    def to_internal_value(self, data):
        return{'url': data}

    class Meta:
        model = Url
        fields = ['url']
        list_serializer_class = UrlListSerializer


class BarcodeListSerializer(BaseListSerializer):
    """Сериализатор списков для модели Barcode"""
    key_fields = ['barcode']


class BarcodeSerializer(SimpleModelSerializer):
    """Сериализатор для модели Barcode"""
    def to_representation(self, instance):
        return instance.barcode

    def to_internal_value(self, data):
        return{'barcode': data}

    class Meta:
        model = Barcode
        fields = ['barcode']
        list_serializer_class = BarcodeListSerializer


class CustomsCommodityCodeListSerializer(BaseListSerializer):
    """Сериализатор списков для модели CustomsCommodityCode"""
    key_fields = ['code']


class CustomsCommodityCodeSerializer(SimpleModelSerializer):
    """Сериализатор для модели CustomsCommodityCode"""
    def to_representation(self, instance):
        return instance.code

    def to_internal_value(self, data):
        return{'code': data}

    class Meta:
        model = CustomsCommodityCode
        fields = ['code']
        list_serializer_class = CustomsCommodityCodeListSerializer


class SupplyScheduleDaysListSerializer(BaseListSerializer):
    """Сериализатор списков для модели SupplyScheduleDays"""
    key_fields = ['supplyScheduleDay']


class SupplyScheduleDaysSerializer(SimpleModelSerializer):
    """Сериализатор для модели SupplyScheduleDays"""
    def to_representation(self, instance):
        return instance.supplyScheduleDay

    def to_internal_value(self, data):
        return{'supplyScheduleDay': data}

    class Meta:
        model = SupplyScheduleDays
        fields = ['supplyScheduleDay']
        list_serializer_class = SupplyScheduleDaysListSerializer


class OfferSerializer(BaseModelSerializer):
    """Сериализатор для модели Offer"""
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
        """Ключ для передачи вложенным моделям"""
        return 'offer'

    class Meta:
        model = Offer
        fields = [
            'shopSku',
            'name',
            'category',
            'manufacturer',
            'manufacturerCountries',
            'weightDimensions',
            'urls',
            'vendor',
            'vendorCode',
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
            'processingState',
        ]
