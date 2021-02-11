from django.db import models

from main.models import TimingTypeChoices, ProcessingStateNoteType, ProcessingStateStatus, MappingType
from main.models.choices import TimeUnitChoices


class ManufacturerCountry(models.Model):
    name = models.CharField(max_length=255, verbose_name='Страна производства товара')


class WeightDimension(models.Model):
    length = models.FloatField(
        verbose_name='Длина упаковки в сантиметрах',
        help_text='Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 65.55'
    )
    width = models.FloatField(
        verbose_name='Ширина упаковки в сантиметрах',
        help_text='Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 50.7'
    )
    height = models.FloatField(
        verbose_name='Высота упаковки в сантиметрах',
        help_text='Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 20.0'
    )
    weight = models.FloatField(
        verbose_name='Вес товара в килограммах',
        help_text='С учетом упаковки (брутто). '
                  'Значение с точностью до тысячных, разделитель целой и дробной части — точка. Пример: 1.001'
    )


class Url(models.Model):
    url = models.CharField(max_length=2000, verbose_name='URL изображения или страницы с описанием товара')


class Barcode(models.Model):
    barcode = models.CharField(max_length=255, verbose_name='Штрихкод товара')


class Timing(models.Model):
    """
    Тайминги товара

    .. todo::
       Добавить проверку на существование максимум трёх таймингов
    """
    time_period = models.BigIntegerField(verbose_name='Срок годности в единицах, указанных в параметре time_unit')
    time_unit = models.CharField(max_length=5, choices=TimeUnitChoices.choices, verbose_name='Единица измерения срока годности')
    comment = models.CharField(
        max_length=2000,
        verbose_name='Дополнительные условия использования в течение срока годности',
        help_text='Например: Хранить в сухом помещении'
    )
    timing_type = models.IntegerField(
        choices=TimingTypeChoices.choices,
        verbose_name='Тип таймингового поля',
        help_text='Определяет, где в каком свойстве модели будет находиться свойство'
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
    code = models.CharField(
        max_length=10,
        verbose_name='Код товара в единой Товарной номенклатуре внешнеэкономической деятельности (ТН ВЭД)',
        help_text='Формат кода: 10 цифр без пробелов'
    )


class ProcessingStateNote(models.Model):
    note_type = models.CharField(
        max_length=31,
        choices=ProcessingStateNoteType.choices,
        verbose_name='Тип причины, по которой товар не прошел модерацию'
    )
    payload = models.CharField(
        max_length=2000,
        verbose_name='Дополнительная информация о причине отклонения товара',
        help_text='Возвращается, если параметр type имеет одно из следующих значений: '
                  'CONFLICTING_INFORMATION, INCORRECT_INFORMATION, NO_PARAMETERS_IN_SHOP_TITLE, NO_SIZE_MEASURE.'
    )


class ProcessingState(models.Model):
    status = models.CharField(
        max_length=12,
        choices=ProcessingStateStatus.choices,
        verbose_name='Статус публикации товара'
    )
    notes = models.ForeignKey(
        to=ProcessingStateNote,
        on_delete=models.CASCADE,
        verbose_name='Причины, по которым товар не прошел модерацию'
    )


class Mapping(models.Model):
    market_sku = models.IntegerField(verbose_name='SKU на Яндексе — идентификатор текущей карточки товара на Маркете')
    model_id = models.IntegerField(
        verbose_name='Идентификатор модели для текущей карточки товара на Маркете',
        help_text='Например, две лопатки разных цветов имеют разные SKU на Яндексе (параметр market_sku), '
                  'но одинаковый идентификатор модели товара'
    )
    category_id = models.IntegerField(verbose_name='Идентификатор категории для текущей карточки товара на Маркете')
    mapping_type = models.CharField(max_length=19, choices=MappingType.choices, verbose_name='Тип маппинга')
