"""
Модель для хранения отчетов по остаткам товаров на складах
docs: https://yandex.ru/dev/market/partner-marketplace/doc/dg/reference/post-campaigns-id-stats-skus.html
"""

from django.db import models
from main.models_addon.ya_market import Offer, Warehouse


class OfferReport(models.Model):
    """
    Модель для хранения отчёта по товару.
    """
    offer = models.OneToOneField(to=Offer, on_delete=models.CASCADE, related_name='report')
    shopSku = models.CharField(max_length=255, verbose_name='Ваш SKU', null=True)
    marketSku = models.PositiveSmallIntegerField(
        verbose_name='SKU на Яндексе — идентификатор текущей карточки товара на Маркете',
        null=True,
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название товара', null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
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
    warehouses = models.ManyToManyField(
        to=Warehouse,
        verbose_name='Информация о складах, на которых хранится товар',
    )

    @property
    def weightDimensions(self):
        """данные о weightDimensions из связанной модели Offer"""
        return self.offer.weightDimentions
