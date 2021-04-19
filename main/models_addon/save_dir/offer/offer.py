"""Паррерн для сохранения данных о товаре в БД"""

from django.core.exceptions import ObjectDoesNotExist

from main.models_addon import Offer, Mapping
from main.models_addon.save_dir.base import BasePattern
from main.serializers import OfferSerializer, MappingSerializer


class OfferPattern(BasePattern):
    """Класс, сохраняющий данные offer из json в БД"""
    MAPPINGS = {
        'mapping': "BASE",
        'awaitingModerationMapping': 'AWAITING_MODERATION',
        'rejectedMapping': 'REJECTED'
    }

    @staticmethod
    def save_mapping(data: dict, offer_instance: Offer, mapping_name: str, mapping_type: str) -> None:
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
                serializer.save(offer=offer_instance, mappingType=mapping_type)
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
                offer_instance = serializer.save(user=user)
                for mapping_name, mapping_type in self.MAPPINGS.items():
                    self.save_mapping(item, offer_instance, mapping_name, mapping_type)
            else:
                print(serializer.errors)
