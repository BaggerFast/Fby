from django.db import models

# from main.models.support import ManufacturerCountry, WeightDimension, Barcode, Timing, CustomsCommodityCode, \
#     ProcessingState, Mapping, Url
from main.models.choices import TimingTypeChoices, AvailabilityChoices, SupplyScheduleDayChoices, MappingType


class Offer(models.Model):
    shop_sku = models.CharField(max_length=255, verbose_name='SKU товара в нашем магазине', null=True)
    name = models.CharField(max_length=255, verbose_name='Название товара', null=True)
    category = models.CharField(max_length=255, verbose_name='Категория товара', null=True)
    manufacturer = models.CharField(
        max_length=255,
        verbose_name='Изготовитель товара',
        help_text='Компания, которая произвела товар, ее адрес и регистрационный номер (если есть)',
        null=True
    )

    vendor = models.CharField(max_length=255, verbose_name='Бренд товара', null=True)
    vendor_code = models.CharField(max_length=255, verbose_name='Артикул товара от производителя', null=True)
    description = models.CharField(max_length=2000, verbose_name='Описание товара', null=True)

    @property
    def shelf_life(self):
        """
        Информация о сроке годности

        Через какое время (в годах, месяцах, днях, неделях или часах)
        товар станет непригоден для использования.
        Например, срок годности есть у таких категорий, как продукты питания и медицинские препараты.
        """
        return self.timings_set.get(timing_type=TimingTypeChoices.SHELF_LIFE)

    @property
    def life_time(self):
        """
        Информация о сроке службы

        В течение какого периода (в годах, месяцах, днях, неделях или часах)
        товар будет исправно выполнять свою функцию,
        а изготовитель — нести ответственность за его существенные недостатки.
        """
        return self.timings_set.get(timing_type=TimingTypeChoices.LIFE_TIME)

    @property
    def guarantee_period(self):
        """
        Информация о гарантийном сроке

        В течение какого периода (в годах, месяцах, днях, неделях или часах)
        возможны обслуживание и ремонт товара или возврат денег,
        а изготовитель или продавец будет нести ответственность за недостатки товара.
        """
        return self.timings_set.get(timing_type=TimingTypeChoices.GUARANTEE_PERIOD)

    certificate = models.CharField(max_length=255,
                                   verbose_name='Номер документа на товар',
                                   help_text='Документ по его номеру можно найти в личном кабинете магазина',
                                   null=True
                                   )
    availability = models.CharField(
        max_length=8,
        choices=AvailabilityChoices.choices,
        verbose_name='Планы по поставкам',
        null=True
    )
    transport_unit_size = models.IntegerField(
        verbose_name='Количество единиц товара в одной упаковке, которую вы поставляете на склад',
        help_text='Например, если вы поставляете детское питание коробками по 6 баночек, значение равно 6',
        null=True
    )
    min_shipment = models.IntegerField(
        verbose_name='Минимальное количество единиц товара, которое вы поставляете на склад',
        help_text='Например, если вы поставляете детское питание партиями минимум по 10 коробок, '
                  'а в каждой коробке по 6 баночек, значение равно 60',
        null=True
    )
    quantum_of_supply = models.IntegerField(
        verbose_name='Добавочная партия: по сколько единиц товара можно добавлять '
                     'к минимальному количеству min_shipment',
        help_text='Например, если вы поставляете детское питание партиями минимум по 10 коробок и хотите добавлять '
                  'к минимальной партии по 2 коробки, а в каждой коробке по 6 баночек, значение равно 12.',
        null=True
    )
    delivery_duration_days = models.IntegerField(verbose_name='Срок, за который вы поставляете товары на склад, в днях', null=True)
    box_count = models.IntegerField(
        verbose_name='Сколько мест (если больше одного) занимает товар',
        help_text='Например, кондиционер занимает два места: внешний и внутренний блоки в двух коробках',
        null=True
    )

    @property
    def shelf_life_days(self):
        """
        Срок годности товара: через сколько дней товар станет непригоден для использования.

        Рассчитывается на основе поля :class:`shelf_life`

        .. todo::
           Добавить функцию-сеттер для этого поля (спасибо Я.API за это)
        """
        return self.shelf_life.get_days()

    @property
    def life_time_days(self):
        """
        Срок службы товара: течение какого периода товар будет исправно выполнять свою функцию,

        Рассчитывается на основе поля :class:`life_time`

        .. todo::
           Добавить функцию-сеттер для этого поля (спасибо Я.API за это)
        """
        return self.life_time.get_days()

    @property
    def guarantee_period_days(self):
        """
        Гарантийный срок товара: в течение какого периода возможны обслуживание и ремонт товара или возврат денег

        Рассчитывается на основе поля :class:`guarantee_period`

        .. todo::
           Добавить функцию-сеттер для этого поля (спасибо Я.API за это)
        """
        return self.guarantee_period.get_days()

    @property
    def processing_state(self):
        """
        Информация о статусе публикации товара на Маркете

        Рассчитывается на основе поля :class:`processing_states`

        .. todo::
           Проверить, что свойство :class:`processing_state` работает нормально
        """
        return self.processing_states_set.last()

    @property
    def mapping(self):
        """
        Информация о текущей карточке товара на Маркете

        .. todo::
           Проверить, что свойство :class:`mapping` работает нормально
        """
        return self.mappings_set.get(mapping_type=MappingType.BASE)

    @property
    def awaiting_moderation_mapping(self):
        """
        Информация о карточке товара на Маркете, проходящей модерацию для данного товара

        .. todo::
           Проверить, что свойство :class:`awaiting_moderation_mapping` работает нормально
        """
        return self.mappings_set.get(mapping_type=MappingType.AWAITING_MODERATION)

    @property
    def rejected_mapping(self):
        """
        Информация о последней карточке товара на Маркете, отклоненной на модерации для данного товара

        .. todo::
           Проверить, что свойство :class:`rejected_mapping` работает нормально
        """
        return self.mappings_set.get(mapping_type=MappingType.REJECTED)


