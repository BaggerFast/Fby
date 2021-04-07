from django.core.exceptions import ValidationError
from django.db import models
from main.models.ya_market.offer.base import Offer
from main.models.ya_market.offer.choices import TimeUnitChoices, MappingType, ProcessingStateNoteType, \
    ProcessingStateStatus, SupplyScheduleDayChoices, VatType


class Timing(models.Model):
    class Meta:
        abstract = True

    offer = models.OneToOneField(
        to=Offer,
        on_delete=models.CASCADE,
    )

    timePeriod = models.PositiveSmallIntegerField(null=True, blank=True)

    timeUnit = models.CharField(max_length=5, choices=TimeUnitChoices.choices, verbose_name='Единица измерения'
                                , null=True, blank=True)

    comment = models.CharField(
        max_length=2000,
        null=True,
        blank=True,
    )

    def get_days(self):
        if self.timeUnit == TimeUnitChoices.HOUR:
            return self.timePeriod / 24
        elif self.timeUnit == TimeUnitChoices.DAY:
            return self.timePeriod
        elif self.timeUnit == TimeUnitChoices.WEEK:
            return self.timePeriod * 7
        elif self.timeUnit == TimeUnitChoices.MONTH:
            return self.timePeriod * 31
        elif self.timeUnit == TimeUnitChoices.YEAR:
            return self.timePeriod * 365


class ShelfLife(Timing):
    # Тут все сделано и работает
    pass


class LifeTime(Timing):
    pass


class GuaranteePeriod(Timing):
    pass


class Price(models.Model):
    discountBase = models.FloatField(verbose_name="Цена на товар без скидки.", null=True, blank=True)
    value = models.FloatField(verbose_name="Цена на товар.", null=True, blank=True)
    vat = models.IntegerField(verbose_name='Идентификатор ставки НДС',
                              help_text="Если параметр не указан, используется ставка НДС, установленная в личном "
                                        "кабинете магазина.",
                              null=True,
                              blank=True,
                              choices=VatType.choices
                              )
    offer = models.OneToOneField(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='price',
    )

    def clean(self):
        if self.discountBase < self.value:
            raise ValidationError({'discountBase': 'Цена на товар без скидки < цены на товар'})
        if self.value <= 0:
            raise ValidationError({'value': 'Должно быть больше нуля'})


class ManufacturerCountry(models.Model):
    """
        .. todo::
           Добавить проверку на то, что в списке товаров может быть максимум 5 стран
    """
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name="manufacturerCountries",
    )
    name = models.CharField(max_length=255, verbose_name='Страна производства товара')


class WeightDimension(models.Model):
    offer = models.OneToOneField(
        to=Offer,
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


class Url(models.Model):
    """
        Список URL
        .. todo::
           Добавить проверку на то, что в списке URL'ов присутствует минимум одна запись
    """
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='urls',
    )
    url = models.URLField(max_length=2000, verbose_name='Ссылка на фото')


class Barcode(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
    )
    barcode = models.CharField(max_length=255, verbose_name='Штрихкод',
                               help_text='Штрихкод обязателен при размещении товара по модели FBY и FBY+. '
                                         'Допустимые форматы: EAN-13, EAN-8, UPC-A, UPC-E, Code 128. Для книг'
                                         ' — ISBN-10 или ISBN-13. Для товаров определённых производителей передайте '
                                         'только код GTIN. Если штрихкодов несколько, укажите их через запятую.',
                               blank=True,
                               null=True)


class CustomsCommodityCode(models.Model):
    offer = models.OneToOneField(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='customsCommodityCodes',
    )
    code = models.CharField(
        max_length=10,
        verbose_name='Код ТН ВЭД',
        help_text='Укажите 10 или 14 цифр без пробелов.', blank=True,
        null=True
    )

    def clean(self):
        if self.code:
            if len(self.code) != 10:
                raise ValidationError({'code': f'Код ТН ВЭД должен содержать 10. У вас {len(self.code)}'})

    def __str__(self):
        return self.code


class SupplyScheduleDays(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name="supplyScheduleDays",
    )
    supplyScheduleDay = models.CharField(
        max_length=9,
        choices=SupplyScheduleDayChoices.choices,
        verbose_name='Дни поставки',
        help_text='Дни недели, когда вы готовы поставлять товары на склад маркетплейса. '
                  'Заполняйте поле, чтобы получать рекомендации о пополнении товаров на складе.',
        null=True
    )

    def __str__(self):
        return self.supplyScheduleDay


class ProcessingState(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='processingState_set',
    )
    status = models.CharField(
        max_length=12,
        choices=ProcessingStateStatus.choices,
        verbose_name='Cтатус',
        help_text="Можно продавать или нет",
        null=True
    )


class ProcessingStateNote(models.Model):
    processingState = models.ForeignKey(
        to=ProcessingState,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Причины, по которым товар не прошел модерацию',
        null=True
    )
    type = models.CharField(
        max_length=31,
        choices=ProcessingStateNoteType.choices,
        verbose_name='Тип причины, по которой товар не прошел модерацию',
        null=True
    )
    payload = models.CharField(
        max_length=2000,
        verbose_name='Дополнительная информация о причине отклонения товара',
        help_text='Возвращается, если параметр type имеет одно из следующих значений: '
                  'CONFLICTING_INFORMATION, INCORRECT_INFORMATION, NO_PARAMETERS_IN_SHOP_TITLE, NO_SIZE_MEASURE.',
        null=True
    )


class Mapping(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name="mapping_set",
    )
    marketSku = models.PositiveSmallIntegerField(
        verbose_name='SKU на Яндексе — идентификатор текущей карточки товара на Маркете',
        null=True,
    )
    modelId = models.PositiveSmallIntegerField(
        verbose_name='Идентификатор модели для текущей карточки товара на Маркете',
        help_text='Например, две лопатки разных цветов имеют разные SKU на Яндексе (параметр market_sku), '
                  'но одинаковый идентификатор модели товара',
        null=True
    )
    categoryId = models.PositiveSmallIntegerField(
        verbose_name='Идентификатор категории для текущей карточки товара на Маркете',
        null=True,
    )
    mappingType = models.CharField(
        max_length=19,
        choices=MappingType.choices,
        verbose_name='Тип маппинга',
        null=True
    )
