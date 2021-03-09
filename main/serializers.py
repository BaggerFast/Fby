"""
Сериализаторы всея моделей

.. todo::
   Дописать все сериализаторы
"""

from rest_framework import serializers

from main.models import Offer, WeightDimension, ManufacturerCountry


class WeightDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightDimension
        fields = ['length', 'width', 'height', 'weight']


class ManufacturerCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerCountry
        fields = ['name']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'shopSku', 'name',
                  'category', 'manufacturer',
                  'weightDimensions', 'manufacturerCountries']
