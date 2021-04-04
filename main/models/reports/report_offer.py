from django.db import models


class Sku(models.Model):
    shopSku = models.CharField(max_length=255, verbose_name='Ваш SKU', null=True)
    marketSku = models.PositiveSmallIntegerField(
        verbose_name='SKU на Яндексе — идентификатор текущей карточки товара на Маркете',
        null=True,
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название товара', null=True)
    price = models.FloatField(
        verbose_name='Цена на товар, выставленная партнером',
        null=True,
        blank=True
    )
    categoryId = models.BigIntegerField(
        verbose_name='Идентификатор категории товара на Маркете',
        null=True,
        blank=True
    )
    categoryName = models.CharField(
        max_length=255,
        verbose_name='Название категории товара на Маркете',
        null=True,
        blank=True
    )
