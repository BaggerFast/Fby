from django.db import models
from django.contrib.auth.models import User

# from main.models import Offer, Warehouse
from main.models.ya_market import Offer, Warehouse


class OfferReport(models.Model):
    """
    Модель хранящая отчёт по товару.
    """
    offer = models.OneToOneField(to=Offer, on_delete=models.CASCADE, related_name='report')
    shopSku = models.CharField(max_length=255, verbose_name='Ваш SKU', null=True)
    marketSku = models.PositiveSmallIntegerField(
        verbose_name='SKU на Яндексе — идентификатор текущей карточки товара на Маркете',
        null=True,
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название товара', null=True)
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
        # on_delete=models.SET_NULL,
        verbose_name='Информация о складах, на которых хранится товар',
        # null=True
    )

    def get_weightDimensions(self):
        return self.offer.weightDimentions
