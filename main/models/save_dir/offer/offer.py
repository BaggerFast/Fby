from django.core.exceptions import ObjectDoesNotExist

from main.models import Offer, Mapping
from main.serializers.offer_price import OfferSerializer, MappingSerializer


class OfferPattern:
    """Класс, сохраняющий данные offer из json в БД"""
    MAPPINGS = {
        'mapping': "BASE",
        'awaitingModerationMapping': 'AWAITING_MODERATION',
        'rejectedMapping': 'REJECTED'
    }

    def __init__(self, json):
        self.json = json

    def save_mapping(self, data, offer_instance, mapping_name, mapping_type):
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

class Base:
    """ для простых данных"""

    def __init__(self, data, offer, name=''):
        self.data = data
        self.offer = offer
        self.name = name

    def save(self) -> None:
        """
        Сохранить данные
        """
        setattr(self.offer, self.name, self.data)

    def exist(self, item):
        return self.data.get(item, None)
