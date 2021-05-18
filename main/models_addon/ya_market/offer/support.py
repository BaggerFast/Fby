"""Вспомогательные модели для модели Offer"""
from django.core.exceptions import ValidationError
from django.db import models
from main.models_addon.ya_market.base import BaseWeightDimension
from main.models_addon.ya_market.offer.base import Offer
from main.models_addon.ya_market.offer.choices import TimeUnitChoices, MappingType, ProcessingStateNoteType, \
    ProcessingStateStatus, SupplyScheduleDayChoices, VatType, CurrencyChoices, PriceSuggestionChoices


class PriceSuggestion(models.Model):
    """
    Модель для хранения цен для продвижения
    """
    offer = models.ForeignKey(to=Offer, on_delete=models.CASCADE, related_name='priceSuggestion')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
        help_text='Указана в рублях. Точность — два знака после запятой',
        null=True)
    type = models.CharField(
        max_length=21,
        choices=PriceSuggestionChoices.choices,
        verbose_name='Типы цен',
        null=True, blank=True)


class Timing(models.Model):
    """
    Модель для хранения периода времени.
    """

    class Meta:
        abstract = True

    timePeriod = models.PositiveSmallIntegerField(null=True, blank=True)
    timeUnit = models.CharField(max_length=5, choices=TimeUnitChoices.choices, verbose_name='Единица измерения',
                                null=True, blank=True)
    comment = models.CharField(max_length=2000, null=True, blank=True)

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
    offer = models.OneToOneField(to=Offer, on_delete=models.CASCADE, related_name='shelfLife')


class LifeTime(Timing):
    offer = models.OneToOneField(to=Offer, on_delete=models.CASCADE, related_name='lifeTime')


class GuaranteePeriod(Timing):
    offer = models.OneToOneField(to=Offer, on_delete=models.CASCADE, related_name='guaranteePeriod')


class Price(models.Model):
    """
    Модель для хранения цены товара.
    """
    offer = models.OneToOneField(to=Offer, on_delete=models.CASCADE, related_name='price')
    currencyId = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        verbose_name='Валюта',
        default=CurrencyChoices.RUR[0][0],
    )
    discountBase = models.FloatField(verbose_name="Цена на товар без скидки.", null=True, blank=True)
    value = models.FloatField(verbose_name="Цена на товар.", null=True, blank=True)
    vat = models.IntegerField(verbose_name='НДС',
                              help_text="Если параметр не указан, используется ставка НДС, "
                                        "установленная в личном кабинете магазина.",
                              null=True,
                              blank=True,
                              choices=VatType.choices
                              )
    net_cost = models.PositiveIntegerField(verbose_name="Себестоимость", null=True, blank=True)
    has_changed = models.BooleanField(verbose_name='Есть изменения, не отправленные на Яндекс',
                                      help_text="True, если изменения есть, False, если изменений нет",
                                      default=True)

    def clean(self):
        if self.discountBase and self.discountBase < self.value:
            raise ValidationError({'discountBase': 'Цена на товар без скидки меньше цены на товар'})
        if self.discountBase is not None and not self.discountBase > 0:
            raise ValidationError({'discountBase': 'Цена на товар без скидки должна быть больше'})


class ManufacturerCountry(models.Model):
    """
    Модель для хранения страны производителя.
    """
    offer = models.ForeignKey(to=Offer, on_delete=models.CASCADE, related_name="manufacturerCountries", )
    name = models.CharField(max_length=255, verbose_name='Страна производства товара')


class WeightDimension(BaseWeightDimension):
    """
    Модель для хранения размеров и веса товара.
    """
    offer = models.OneToOneField(to=Offer, on_delete=models.CASCADE, related_name='weightDimensions')


class Url(models.Model):
    """
    Модель для хранения списка URL
    """
    offer = models.ForeignKey(to=Offer, on_delete=models.CASCADE, related_name='urls')
    url = models.URLField(max_length=2000, verbose_name='Ссылка на фото')


class Barcode(models.Model):
    """
    Модель для хранения штрихкода товара.
    """
    offer = models.ForeignKey(to=Offer, on_delete=models.CASCADE, related_name='barcodes')
    barcode = models.CharField(max_length=255, verbose_name='Штрихкод',
                               help_text="""Штрихкод обязателен при размещении товара по модели FBY и FBY+.
                                         Допустимые форматы: EAN-13, EAN-8, UPC-A, UPC-E, Code 128. Для книг
                                          — ISBN-10 или ISBN-13. Для товаров определённых производителей передайте
                                         только код GTIN. Если штрихкодов несколько, укажите их через запятую.""",
                               )


class CustomsCommodityCode(models.Model):
    """
    Модель для хранения кода ТН ВЭД товара.
    """
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='customsCommodityCodes',
    )
    code = models.CharField(max_length=10, verbose_name='Код ТН ВЭД', help_text='Укажите 10 или 14 цифр без пробелов.',
                            blank=True, null=True)

    def __str__(self):
        return self.code


class SupplyScheduleDays(models.Model):
    """
    Модель для хранения дней поставки товара.
    """
    offer = models.ForeignKey(to=Offer, on_delete=models.CASCADE, related_name="supplyScheduleDays")
    supplyScheduleDay = models.CharField(
        max_length=9,
        choices=SupplyScheduleDayChoices.choices,
        verbose_name='Дни поставки',
        help_text='Дни недели, когда вы готовы поставлять товары на склад маркетплейса.'
                  'Заполняйте поле, чтобы получать рекомендации о пополнении товаров на складе.',
        null=True
    )

    def __str__(self):
        return self.supplyScheduleDay


class ProcessingState(models.Model):
    """
    Модель для хранения статуса товара.
    """
    offer = models.OneToOneField(to=Offer, on_delete=models.CASCADE, related_name='processingState')
    status = models.CharField(
        max_length=12,
        choices=ProcessingStateStatus.choices,
        verbose_name='Cтатус',
        help_text="Можно продавать или нет",
        null=True
    )

    @property
    def get_notes(self):
        return self.notes.all()


class ProcessingStateNote(models.Model):
    """
    Модель для хранения причины, по который товар не прошел модерацию.
    """
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
    """
    Модель для хранения маппинга товара.
    """
    offer = models.ForeignKey(to=Offer, on_delete=models.CASCADE, related_name="mapping_set")
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
