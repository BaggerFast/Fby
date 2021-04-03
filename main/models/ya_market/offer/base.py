from django.db import models
from django.contrib.auth.models import User
from main.models.ya_market.offer.choices import AvailabilityChoices, MappingType


class Offer(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="offer",
        verbose_name="Пользователь",
    )

    marketSku = models.CharField(max_length=255, verbose_name="SKU на Яндексе", null=True, blank=True)

    updatedAt = models.DateTimeField(verbose_name="Дата и время последнего обновления цены на товар", null=True)

    shopSku = models.CharField(max_length=255, verbose_name='Ваш SKU', null=True)

    name = models.CharField(max_length=255,
                            help_text='Составляйте по схеме: тип товара + бренд или производитель + модель + '
                                      'отличительные характеристики.',
                            verbose_name='Название товара', null=True)

    category = models.CharField(max_length=255, verbose_name='Категория', null=True)

    manufacturer = models.CharField(
        max_length=255,
        verbose_name='Изготовитель',
        help_text='Компания, которая произвела товар, ее адрес и регистрационный номер (если есть)', null=True
    )

    vendor = models.CharField(max_length=255, verbose_name='Торговая марка', null=True)

    vendorCode = models.CharField(max_length=255, verbose_name='Артикул производителя', null=True, blank=True)

    description = models.CharField(max_length=2000, verbose_name='Описание товара', null=True, blank=True)

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
        blank=True,
        null=True
    )

    # done
    transportUnitSize = models.PositiveSmallIntegerField(
        verbose_name='Количество товаров в упаковке',
        help_text='Сколько товаров в упаковке. Поле используется, если вы поставляете товар упаковками,'
                  ' а продаете поштучно. Например, вы продаете детское питание по 1 баночке, '
                  'а коробка содержит 6 баночек.',
        blank=True,
        null=True
    )

    minShipment = models.PositiveSmallIntegerField(
        verbose_name='Минимальная партия поставки',
        help_text='Минимальное количество товаров, которое вы готовы привозить на склад. '
                  'Например, если вы поставляете детское питание партиями минимум по 10 коробок,'
                  ' а в каждой коробке по 6 баночек, то ваша минимальная партия — 60 баночек.',
        blank=True,
        null=True
    )

    quantumOfSupply = models.PositiveSmallIntegerField(
        verbose_name='Добавочная партия',
        help_text="По сколько товаров можно добавлять к минимальной партии. Например, вы планируете поставлять"
                  " детское питание партиями, причем к минимальной партии хотите прибавлять минимум по 2 коробки, "
                  "а в каждой коробке по 6 баночек. Тогда добавочная партия — 12 баночек, а к минимальной партии "
                  "можно добавлять 12, 24, 36 баночек и т. д.",
        blank=True,
        null=True
    )

    deliveryDurationDays = models.PositiveSmallIntegerField(verbose_name='Срок поставки',
                                                            help_text="За какое время вы поставите товар на склад.(в днях)",
                                                            null=True,
                                                            blank=True)

    boxCount = models.PositiveIntegerField(verbose_name='Товар занимает больше одного места',
                                           help_text='Если нет — оставьте поле пустым. Если да — укажите количество мест '
                                                     '(например, кондиционер занимает 2 грузовых места — внешний и внутренний блоки в двух коробках).',
                                           blank=True,
                                           null=True

                                           )


    class Meta:
        ordering = ['id']

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
