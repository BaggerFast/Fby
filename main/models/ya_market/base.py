from django.db import models
from main.models.ya_market.choices import TimingTypeChoices, AvailabilityChoices, MappingType


class Offer(models.Model):
    shopSku = models.CharField(max_length=255, verbose_name='SKU товара в нашем магазине', null=True)
    name = models.CharField(max_length=255, verbose_name='Название товара', null=True)
    category = models.CharField(max_length=255, verbose_name='Категория товара', null=True)
    manufacturer = models.CharField(
        max_length=255,
        verbose_name='Изготовитель товара',
        help_text='Компания, которая произвела товар, ее адрес и регистрационный номер (если есть)',
        null=True
    )

    class Meta:
        ordering = ['id']

    vendor = models.CharField(max_length=255, verbose_name='Бренд товара', null=True)
    vendorCode = models.CharField(max_length=255, verbose_name='Артикул товара от производителя', null=True)
    description = models.CharField(max_length=2000, verbose_name='Описание товара', null=True)

    certificate = models.CharField(
        max_length=255,
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
    transportUnitSize = models.IntegerField(
        verbose_name='Количество единиц товара в одной упаковке, которую вы поставляете на склад',
        help_text='Например, если вы поставляете детское питание коробками по 6 баночек, значение равно 6',
        null=True
    )
    minShipment = models.IntegerField(
        verbose_name='Минимальное количество единиц товара, которое вы поставляете на склад',
        help_text='Например, если вы поставляете детское питание партиями минимум по 10 коробок, '
                  'а в каждой коробке по 6 баночек, значение равно 60',
        null=True
    )
    quantumOfSupply = models.IntegerField(
        verbose_name='Добавочная партия: по сколько единиц товара можно добавлять '
                     'к минимальному количеству min_shipment',
        help_text='Например, если вы поставляете детское питание партиями минимум по 10 коробок и хотите добавлять '
                  'к минимальной партии по 2 коробки, а в каждой коробке по 6 баночек, значение равно 12.',
        null=True
    )
    deliveryDurationDays = models.IntegerField(verbose_name='Срок, за который вы поставляете товары на склад, в днях',
                                               null=True)
    boxCount = models.IntegerField(
        verbose_name='Сколько мест (если больше одного) занимает товар',
        help_text='Например, кондиционер занимает два места: внешний и внутренний блоки в двух коробках',
        null=True
    )

    @property
    def shelfLife(self):
        """
        Информация о сроке годности

        Через какое время (в годах, месяцах, днях, неделях или часах)
        товар станет непригоден для использования.
        Например, срок годности есть у таких категорий, как продукты питания и медицинские препараты.
        """
        return self.timings.get(timingType=TimingTypeChoices.SHELF_LIFE)

    @property
    def lifeTime(self):
        """
        Информация о сроке службы

        В течение какого периода (в годах, месяцах, днях, неделях или часах)
        товар будет исправно выполнять свою функцию,
        а изготовитель — нести ответственность за его существенные недостатки.
        """
        return self.timings.get(timingType=TimingTypeChoices.LIFE_TIME)

    @property
    def guaranteePeriod(self):
        """
        Информация о гарантийном сроке

        В течение какого периода (в годах, месяцах, днях, неделях или часах)
        возможны обслуживание и ремонт товара или возврат денег,
        а изготовитель или продавец будет нести ответственность за недостатки товара.
        """
        return self.timings.get(timingType=TimingTypeChoices.GUARANTEE_PERIOD)

    @property
    def shelfLifeDays(self):
        """
        Срок годности товара: через сколько дней товар станет непригоден для использования.

        Рассчитывается на основе поля :class:`shelfLife`

        .. todo::
           Добавить функцию-сеттер для этого поля (спасибо Я.API за это)
        """
        return self.shelfLife.get_days()

    @property
    def lifeTimeDays(self):
        """
        Срок службы товара: течение какого периода товар будет исправно выполнять свою функцию,

        Рассчитывается на основе поля :class:`lifeTime`

        .. todo::
           Добавить функцию-сеттер для этого поля (спасибо Я.API за это)
        """
        return self.lifeTime.get_days()

    @property
    def guaranteePeriodDays(self):
        """
        Гарантийный срок товара: в течение какого периода возможны обслуживание и ремонт товара или возврат денег

        Рассчитывается на основе поля :class:`guaranteePeriod`

        .. todo::
           Добавить функцию-сеттер для этого поля (спасибо Я.API за это)
        """
        return self.guaranteePeriod.get_days()

    @property
    def processingState(self):
        """
        Информация о статусе публикации товара на Маркете

        Рассчитывается на основе поля :class:`processingState_set`. Берётся последнее значение.
        """
        return self.processingState_set.last()

    @property
    def mapping(self):
        """Информация о текущей карточке товара на Маркете"""
        return self.mapping_set.get(mappingType=MappingType.BASE)

    @property
    def awaitingModerationMapping(self):
        """Информация о карточке товара на Маркете, проходящей модерацию для данного товара"""
        return self.mapping_set.get(mappingType=MappingType.AWAITING_MODERATION)

    @property
    def rejectedMapping(self):
        """Информация о последней карточке товара на Маркете, отклоненной на модерации для данного товара"""
        return self.mapping_set.get(mappingType=MappingType.REJECTED)
