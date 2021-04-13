from django.db import models


class BaseWeightDimension(models.Model):
    """
    Модель хранящая размеры товара.
    """
    class Meta:
        abstract = True

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
