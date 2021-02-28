from django.db import models
from main.models.base import Offer
from main.models.choices import TimeUnitChoices, MappingType, TimingTypeChoices, ProcessingStateNoteType, \
    ProcessingStateStatus, SupplyScheduleDayChoices


class ManufacturerCountry(models.Model):
    """
        Список стран, в которых произведен товар

        .. todo::
           Добавить проверку на то, что в списке товаров может быть максимум 5 стран
    """
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name="manufacturer_countries",
        verbose_name='Список стран, в которых произведен товар',
        help_text='Содержит от одной до 5 стран',
        null=True
    )
    name = models.CharField(max_length=255, verbose_name='Страна производства товара', null=True)


class WeightDimension(models.Model):
    offer = models.OneToOneField(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='weight_dimensions',
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


class Barcode(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        verbose_name='Штрихкоды товара',
        related_name='barcodes',
        null=True
    )
    barcode = models.CharField(max_length=255, verbose_name='Штрихкод товара', null=True)


class Timing(models.Model):
    """
        Тайминги товара

        .. todo::
           Добавить проверку на существование минимум одного тайминга (подозреваю, что Яндекс всё равно их запросит)
        .. todo::
           Проверить, что свойства :class:`shelf_life`, :class:`life_time` и :class:`guarantee_period` работают нормально
        .. todo::
           Добавить проверку на существование максимум трёх таймингов

    """

    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        verbose_name='Тайминги товара',
        related_name='timing',
        help_text='Срок годности, срок службы, гарантийный срок',
        null=True
    )

    time_period = models.BigIntegerField(verbose_name='Срок годности в единицах, указанных в параметре time_unit', null=True)
    time_unit = models.CharField(max_length=5, choices=TimeUnitChoices.choices, verbose_name='Единица измерения срока годности', null=True)
    comment = models.CharField(
        max_length=2000,
        verbose_name='Дополнительные условия использования в течение срока годности',
        help_text='Например: Хранить в сухом помещении',
        null=True
    )
    timing_type = models.IntegerField(
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
        if self.time_unit == TimeUnitChoices.HOUR:
            return self.time_period / 24
        elif self.time_unit == TimeUnitChoices.DAY:
            return self.time_period
        elif self.time_unit == TimeUnitChoices.WEEK:
            return self.time_period * 7
        elif self.time_unit == TimeUnitChoices.MONTH:
            return self.time_period * 31
        elif self.time_unit == TimeUnitChoices.YEAR:
            return self.time_period * 365


class CustomsCommodityCode(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='customs_commodity_code',
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


class ProcessingState(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='processing_state',
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
    processing_state = models.ForeignKey(
        to=ProcessingState,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name='Причины, по которым товар не прошел модерацию',
        null=True
    )
    note_type = models.CharField(
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
        related_name="mapping",
        verbose_name='Привязки карточек на Я.Маркете',
        null=True
    )
    market_sku = models.IntegerField(
        verbose_name='SKU на Яндексе — идентификатор текущей карточки товара на Маркете',
        null=True
    )
    model_id = models.IntegerField(
        verbose_name='Идентификатор модели для текущей карточки товара на Маркете',
        help_text='Например, две лопатки разных цветов имеют разные SKU на Яндексе (параметр market_sku), '
                  'но одинаковый идентификатор модели товара',
        null=True
    )
    category_id = models.IntegerField(
        verbose_name='Идентификатор категории для текущей карточки товара на Маркете',
        null=True,
    )
    mapping_type = models.CharField(
        max_length=19,
        choices=MappingType.choices,
        verbose_name='Тип маппинга',
        null=True
    )


class SupplyScheduleDays(models.Model):
    offer = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        # TODO: добавить описание к related_name
        related_name="supply_schedule_days", verbose_name="",
        null=True
    )
    supply_schedule_day = models.CharField(
        max_length=9,
        choices=SupplyScheduleDayChoices.choices,
        verbose_name='День недели, в который вы поставляете товары на склад',
        null=True
    )
