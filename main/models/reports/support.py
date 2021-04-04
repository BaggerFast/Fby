from django.db import models
from main.models.reports.choices import StockTypeChoices, StorageTypeChoices, InclusionTypeChoices, TariffTypeChoices
from main.models.reports.report_offer import Sku


# Небольшое пояснение - здесь копипаста ya_market/offer/support с изменением Foreign Keys, т.к. класс оффера для
# отчёта немного отличается от настоящего, поэтому тут нельзя исользовать обычный оффер. Также может быть возможно в
# теории использование полиморфизма на те доп. классы(ну типо изменить одно лишь Foreign Key поле.
class WeightDimensions(models.Model):
    report = models.ForeignKey(
        to=Sku,
        on_delete=models.CASCADE,
        related_name='weightDimensions',
    )
    length = models.FloatField(
        verbose_name='Длина, см',
        help_text='Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 65.55',
        null=True,
        blank=True,
    )
    width = models.FloatField(
        verbose_name='Ширина, см',
        help_text='Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 50.7',
        null=True,
        blank=True,
    )
    height = models.FloatField(
        verbose_name='Высота, см',
        help_text='Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 20.0',
        null=True,
        blank=True,
    )
    weight = models.FloatField(
        verbose_name='Вес в упаковке (брутто), кг',
        help_text='С учетом упаковки (брутто). '
                  'Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 1.001',
        null=True,
        blank=True,
    )


class Hiding(models.Model):
    report = models.ForeignKey(
        to=Sku,
        on_delete=models.CASCADE
    )
    type = models.CharField(
        verbose_name='Тип сообщения о скрытии вашего предложения',
        null=True,
        blank=True
    )
    code = models.CharField(
        verbose_name='Код сообщения о скрытии вашего предложения',
        null=True,
        blank=True
    )
    message = models.TextField(
        verbose_name='Сообщение о скрытии вашего предложения',
        null=True,
        blank=True
    )
    comment = models.CharField(
        verbose_name='Комментарий к сообщению о скрытии вашего предложения',
        null=True,
        blank=True
    )


class Warehouse(models.Model):
    report = models.ForeignKey(
        to=Sku,
        on_delete=models.CASCADE
    )
    id = models.PositiveSmallIntegerField(
        verbose_name='Идентификатор склада',
        null=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название товара',
        null=True
    )


class Stock(models.Model):
    warehouse = models.ForeignKey(
        to=Warehouse,
        on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=9,
        choices=StockTypeChoices.choices,
        verbose_name='Тип остатков товаров на складе',
        null=True
    )
    count = models.BigIntegerField(
        verbose_name='Количество товара для указанного типа остатков на складе',
        null=True,
    )


class Storage(models.Model):
    report = models.ForeignKey(
        to=Sku,
        on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=4,
        choices=StorageTypeChoices.choices,
        verbose_name='Тип условий хранения и обработки товара на складе',
        null=True
    )
    count = models.BigIntegerField(
        verbose_name='Количество товара для указанного типа условий хранения и обработки товара на складе',
        null=True,
    )


class Inclusion(models.Model):
    storage = models.ForeignKey(
        to=Storage,
        on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=11,
        choices=InclusionTypeChoices.choices,
        verbose_name='Тип условий хранения и обработки товара на складе',
        null=True
    )
    count = models.BigIntegerField(
        verbose_name='Количество товара для указанного типа условий хранения и обработки товара на складе',
        null=True,
    )


class Tariff(models.Model):
    report = models.ForeignKey(
        to=Sku,
        on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=17,
        choices=TariffTypeChoices.choices,
        verbose_name='Тип остатков товаров на складе',
        null=True
    )
    percent = models.FloatField(
        verbose_name='Значение тарифа в процентах',
        null=True,
        blank=True
    )
    amount = models.FloatField(
        verbose_name='Значение тарифа в рублях',
        null=True,
        blank=True
    )
