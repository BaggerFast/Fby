from django.db import models
from main.models.ya_market.base import Offer
from main.models.ya_market.choices import TimeUnitChoices, MappingType, TimingTypeChoices, ProcessingStateNoteType, \
    ProcessingStateStatus, SupplyScheduleDayChoices


class Price(models.Model):
    shopSku = models.CharField(max_length=255, null=True)
    marketSku = models.IntegerField(null=True)
    updatedAt = models.DateTimeField(verbose_name="Дата и время последнего обновления цены на товар", null=True)
    discountBase = models.FloatField(verbose_name="Цена на товар без скидки.", null=True)
    value = models.FloatField(verbose_name="Цена на товар.", null=True)
    vat = models.IntegerField(
        verbose_name="""
            Идентификатор ставки НДС, применяемой для товара:
            2 — 10%.
            5 — 0%.
            6 — не облагается НДС.
            7 — 20%.
            Если параметр не указан, используется ставка НДС, установленная в личном кабинете магазина.
            """,
        null=True
    )

    offer = models.OneToOneField(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='priceData',
        verbose_name='Данные о цене',
        null=True
    )


class ManufacturerCountry(models.Model):
    """
        Список стран, в которых произведен товар

        .. todo::
           Добавить проверку на то, что в списке товаров может быть максимум 5 стран
    """
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name="manufacturerCountries",
        verbose_name='Список стран, в которых произведен товар',
        help_text='Содержит от одной до 5 стран',
        null=True
    )
    name = models.CharField(max_length=255, verbose_name='Страна производства товара', null=True)

    def __str__(self):
        return self.name


class WeightDimension(models.Model):
    offer = models.OneToOneField(
        to=Price,
        on_delete=models.CASCADE,
        related_name='weightDimensions',
        verbose_name='Габариты упаковки и вес товара',
        null=True
    )
    length = models.FloatField(
        verbose_name='Длина упаковки в сантиметрах',
        help_text='Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 65.55',
        null=True
    )
    width = models.FloatField(
        verbose_name='Ширина упаковки в сантиметрах',
        help_text='Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 50.7',
        null=True
    )
    height = models.FloatField(
        verbose_name='Высота упаковки в сантиметрах',
        help_text='Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 20.0',
        null=True
    )
    weight = models.FloatField(
        verbose_name='Вес товара в килограммах',
        help_text='С учетом упаковки (брутто). '
                  'Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 1.001',
        null=True
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
        verbose_name='Список URL',
        help_text='страниц с описанием товара на вашем сайте; '
                  'фотографий товара в хорошем качестве. '
                  'Содержит хотя бы один URL',
        null=True
    )
    url = models.CharField(max_length=2000, verbose_name='URL изображения или страницы с описанием товара', null=True)

    def __str__(self):
        return self.url


class Barcode(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        verbose_name='Штрихкоды товара',
        related_name='barcodes',
        null=True
    )
    barcode = models.CharField(max_length=255, verbose_name='Штрихкод товара', null=True)

    def __str__(self):
        return self.barcode


class Timing(models.Model):
    """
        Тайминги товара

        .. todo::
           Добавить проверку на существование минимум одного тайминга (подозреваю, что Яндекс всё равно их запросит)
        .. todo::
           Добавить проверку на существование максимум трёх таймингов

    """

    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        verbose_name='Тайминги товара',
        related_name='timings',
        help_text='Срок годности, срок службы, гарантийный срок',
        null=True
    )

    timePeriod = models.BigIntegerField(verbose_name='Срок годности в единицах, указанных в параметре time_unit',
                                        null=True)
    timeUnit = models.CharField(max_length=5, choices=TimeUnitChoices.choices,
                                verbose_name='Единица измерения срока годности', null=True)
    comment = models.CharField(
        max_length=2000,
        verbose_name='Дополнительные условия использования в течение срока годности',
        help_text='Например: Хранить в сухом помещении',
        null=True
    )
    timingType = models.IntegerField(
        choices=TimingTypeChoices.choices,
        verbose_name='Тип таймингового поля',
        help_text='Определяет, где в каком свойстве модели будет находиться свойство',
        null=True
    )
    """
    Тип таймингового поля
    
    .. todo::
       Добавить проверку на то, что в списке таймингов нет элементов 
       с повторяющимся полем :class:`timing_type` для одного товара
       Например, чтобы у товара не было двух сроков годности.
    """

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


class CustomsCommodityCode(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='customsCommodityCodes',
        verbose_name='Список кодов товара в единой ТН ВЭД',
        help_text='Список кодов товара в единой Товарной номенклатуре внешнеэкономической деятельности (ТН ВЭД), '
                  'если товар подлежит особому учету (например, в системе "Меркурий" как продукция '
                  'животного происхождения или в системе "Честный ЗНАК"). '
                  'Может содержать только один вложенный код ТН ВЭД.',
        null=True
    )
    code = models.CharField(
        max_length=10,
        verbose_name='Код товара в единой Товарной номенклатуре внешнеэкономической деятельности (ТН ВЭД)',
        help_text='Формат кода: 10 цифр без пробелов',
        null=True
    )

    def __str__(self):
        return self.code


class SupplyScheduleDays(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name="supplyScheduleDays",
        verbose_name="День недели, в который вы поставляете товары на склад",
        null=True
    )
    supplyScheduleDay = models.CharField(
        max_length=9,
        choices=SupplyScheduleDayChoices.choices,
        verbose_name='День недели, в который вы поставляете товары на склад',
        null=True
    )

    def __str__(self):
        return self.supplyScheduleDay


class ProcessingState(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='processingState_set',
        verbose_name='История статусов публикации товара на Маркете',
        null=True
    )
    status = models.CharField(
        max_length=12,
        choices=ProcessingStateStatus.choices,
        verbose_name='Статус публикации товара',
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
        verbose_name='Привязки карточек на Я.Маркете',
        null=True
    )
    marketSku = models.IntegerField(
        verbose_name='SKU на Яндексе — идентификатор текущей карточки товара на Маркете',
        null=True
    )
    modelId = models.IntegerField(
        verbose_name='Идентификатор модели для текущей карточки товара на Маркете',
        help_text='Например, две лопатки разных цветов имеют разные SKU на Яндексе (параметр market_sku), '
                  'но одинаковый идентификатор модели товара',
        null=True
    )
    categoryId = models.IntegerField(
        verbose_name='Идентификатор категории для текущей карточки товара на Маркете',
        null=True,
    )
    mappingType = models.CharField(
        max_length=19,
        choices=MappingType.choices,
        verbose_name='Тип маппинга',
        null=True
    )
