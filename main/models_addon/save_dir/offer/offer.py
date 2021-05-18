"""Паррерн для сохранения данных о товаре в БД"""

from django.core.exceptions import ObjectDoesNotExist

from main.models_addon.ya_market import Offer, Mapping, SupplyScheduleDays, CustomsCommodityCode, Barcode, Url, \
    ManufacturerCountry, ProcessingState, ProcessingStateNote, GuaranteePeriod, LifeTime, ShelfLife, WeightDimension, \
    Price
from main.models_addon.save_dir.base import BasePattern
from main.serializers import OfferSerializer, MappingSerializer


class OfferPattern(BasePattern):
    """
    Класс, сохраняющий данные offer из json в БД
    """
    MAPPINGS = {
        'mapping': "BASE",
        'awaitingModerationMapping': 'AWAITING_MODERATION',
        'rejectedMapping': 'REJECTED'
    }
    MODELS = {
        Offer: {
            'unique_fields': ['shopSku', 'user'],
            'update_fields': ['name', 'category', 'manufacturer',
                              'vendor', 'vendorCode', 'certificate',
                              'availability', 'transportUnitSize',
                              'minShipment', 'quantumOfSupply',
                              'deliveryDurationDays', 'boxCount']
        },
        SupplyScheduleDays: {
            'unique_fields': ['offer', 'supplyScheduleDay'],
            'update_fields': []
        },
        CustomsCommodityCode: {
            'unique_fields': ['offer', 'code'],
            'update_fields': []
        },
        Barcode: {
            'unique_fields': ['offer', 'barcode'],
            'update_fields': []
        },
        Url: {
            'unique_fields': ['offer', 'url'],
            'update_fields': []
        },
        ManufacturerCountry: {
            'unique_fields': ['offer', 'name'],
            'update_fields': []
        },
        ProcessingState: {
            'unique_fields': ['offer'],
            'update_fields': ['status']
        },
        ProcessingStateNote: {
            'unique_fields': ['processingState', 'type'],
            'update_fields': ['payload']
        },
        GuaranteePeriod: {
            'unique_fields': ['offer'],
            'update_fields': ['timePeriod', 'timeUnit', 'comment']
        },
        LifeTime: {
            'unique_fields': ['offer'],
            'update_fields': ['timePeriod', 'timeUnit', 'comment']
        },
        ShelfLife: {
            'unique_fields': ['offer'],
            'update_fields': ['timePeriod', 'timeUnit', 'comment']
        },
        WeightDimension: {
            'unique_fields': ['offer'],
            'update_fields': ['length', 'width', 'height', 'weight']
        },
        Mapping: {
            'unique_fields': ['offer', 'mappingType'],
            'update_fields': ['marketSku', 'modelId', 'categoryId']
        },
    }

    def save_mapping(self, data: dict, offer_instance: Offer, mapping_name: str, mapping_type: str) -> None:
        """Сохраняет карточку товара (маппинг)

        Если в бд есть карточка, которой нет в json-данных, удаляет ее из бд
        """
        if mapping_name in data:
            try:
                instance = Mapping.objects.get(offer=offer_instance, mappingType=mapping_type)
                serializer = MappingSerializer(instance=instance, data=data[mapping_name])
            except ObjectDoesNotExist:
                serializer = MappingSerializer(data=data[mapping_name])
            if serializer.is_valid():
                if mapping_name == 'mapping':
                    market_sku = data['mapping'].get('marketSku', None)
                    if market_sku and getattr(offer_instance, 'marketSku', None) != market_sku:
                        offer_instance.marketSku = market_sku
                        offer_instance.save(update_fields=['marketSku'])
                serializer.save(offer=offer_instance, mappingType=mapping_type)
                self.created_objects.extend(serializer.created_objs)
                self.updated_objects.extend(serializer.updated_objs)
            else:
                print(serializer.errors)
        else:
            try:
                instance = Mapping.objects.get(offer=offer_instance, mappingType=mapping_type)
                instance.delete()
            except ObjectDoesNotExist:
                pass

    def save(self, user):
        """Сохраняет товары"""
        for item in self.json:
            try:
                instance = Offer.objects.get(shopSku=item['offer'].get('shopSku'), user=user)
                serializer = OfferSerializer(instance=instance, data=item['offer'])
            except ObjectDoesNotExist:
                serializer = OfferSerializer(data=item['offer'])

            if serializer.is_valid():
                offer_instance = serializer.save(user=user, has_changed=False)
                self.created_objects.extend(serializer.created_objs)
                self.updated_objects.extend(serializer.updated_objs)
                for mapping_name, mapping_type in self.MAPPINGS.items():
                    self.save_mapping(item, offer_instance, mapping_name, mapping_type)
            else:
                print(serializer.errors)

        self.bulk_create_update()
