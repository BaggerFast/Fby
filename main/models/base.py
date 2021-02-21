from django.db import models

from main.models import ManufacturerCountry, WeightDimension, Barcode, Timing, CustomsCommodityCode, \
    ProcessingState, MappingType, Mapping, Url
from main.models.choices import TimingTypeChoices, AvailabilityChoices, SupplyScheduleDayChoices


class Offer(models.Model):
    shop_sku = models.CharField(max_length=255, verbose_name='SKU товара в нашем магазине')
    name = models.CharField(max_length=255, verbose_name='Название товара')
    category = models.CharField(max_length=255, verbose_name='Категория товара')
    manufacturer = models.CharField(
        max_length=255,
        verbose_name='Изготовитель товара',
        help_text='Компания, которая произвела товар, ее адрес и регистрационный номер (если есть)'
    )
    manufacturer_countries = models.ManyToManyField(
        to=ManufacturerCountry,
        verbose_name='Список стран, в которых произведен товар',
        help_text='Содержит от одной до 5 стран'
    )
    """
    Список стран, в которых произведен товар

    .. todo:: 
       Добавить проверку на то, что в списке товаров может быть максимум 5 стран
    """
    weight_dimensions = models.ForeignKey(
        to=WeightDimension,
        on_delete=models.CASCADE,
        related_name='weight_dimensions',
        verbose_name='Габариты упаковки и вес товара'
    )
    urls = models.ForeignKey(
        to=Url,
        on_delete=models.CASCADE,
        related_name='urls',
        verbose_name='Список URL',
        help_text='страниц с описанием товара на вашем сайте; '
                  'фотографий товара в хорошем качестве. '
                  'Содержит хотя бы один URL'
    )
    """
    Список URL

    .. todo:: 
       Добавить проверку на то, что в списке URL'ов присутствует минимум одна запись
    """
    timings = models.ForeignKey(
        to=Timing,
        on_delete=models.CASCADE,
        verbose_name='Тайминги товара',
        help_text='Срок годности, срок службы, гарантийный срок'
    )
    """
    Тайминги товара

    .. todo::
       Добавить проверку на существование минимум одного тайминга (подозреваю, что Яндекс всё равно их запросит)
    .. todo::
       Проверить, что свойства :class:`shelf_life`, :class:`life_time` и :class:`guarantee_period` работают нормально
    """

    barcodes = models.ForeignKey(to=Barcode, on_delete=models.CASCADE, verbose_name='Штрихкоды товара')
    vendor = models.CharField(max_length=255, verbose_name='Бренд товара')
    vendor_code = models.CharField(max_length=255, verbose_name='Артикул товара от производителя')
    description = models.CharField(max_length=2000, verbose_name='Описание товара')

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

    customs_commodity_codes = models.ForeignKey(
        to=CustomsCommodityCode,
        on_delete=models.CASCADE,
        verbose_name='Список кодов товара в единой ТН ВЭД',
        help_text='Список кодов товара в единой Товарной номенклатуре внешнеэкономической деятельности (ТН ВЭД), '
                  'если товар подлежит особому учету (например, в системе "Меркурий" как продукция '
                  'животного происхождения или в системе "Честный ЗНАК"). '
                  'Может содержать только один вложенный код ТН ВЭД.'
    )
    certificate = models.CharField(max_length=255,
                                   verbose_name='Номер документа на товар',
                                   help_text='Документ по его номеру можно найти в личном кабинете магазина'
                                   )
    availability = models.CharField(
        max_length=8,
        choices=AvailabilityChoices.choices,
        verbose_name='Планы по поставкам'
    )
    transport_unit_size = models.IntegerField(
        verbose_name='Количество единиц товара в одной упаковке, которую вы поставляете на склад',
        help_text='Например, если вы поставляете детское питание коробками по 6 баночек, значение равно 6'
    )
    min_shipment = models.IntegerField(
        verbose_name='Минимальное количество единиц товара, которое вы поставляете на склад',
        help_text='Например, если вы поставляете детское питание партиями минимум по 10 коробок, '
                  'а в каждой коробке по 6 баночек, значение равно 60'
    )
    quantum_of_supply = models.IntegerField(
        verbose_name='Добавочная партия: по сколько единиц товара можно добавлять '
                     'к минимальному количеству min_shipment',
        help_text='Например, если вы поставляете детское питание партиями минимум по 10 коробок и хотите добавлять '
                  'к минимальной партии по 2 коробки, а в каждой коробке по 6 баночек, значение равно 12.'
    )
    supply_schedule_days = models.CharField(
        max_length=9,
        choices=SupplyScheduleDayChoices.choices,
        verbose_name='День недели, в который вы поставляете товары на склад'
    )
    delivery_duration_days = models.IntegerField(verbose_name='Срок, за который вы поставляете товары на склад, в днях')
    box_count = models.IntegerField(
        default=1,
        verbose_name='Сколько мест (если больше одного) занимает товар',
        help_text='Например, кондиционер занимает два места: внешний и внутренний блоки в двух коробках'
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

    processing_states = models.ForeignKey(
        to=ProcessingState,
        on_delete=models.CASCADE,
        verbose_name='История статусов публикации товара на Маркете'
    )

    @property
    def processing_state(self):
        """
        Информация о статусе публикации товара на Маркете

        Рассчитывается на основе поля :class:`processing_states`

        .. todo::
           Проверить, что свойство :class:`processing_state` работает нормально
        """
        return self.processing_states_set.last()

    mappings = models.ForeignKey(to=Mapping, on_delete=models.CASCADE, verbose_name='Привязки карточек на Я.Маркете')

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
