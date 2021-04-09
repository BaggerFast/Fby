from django.contrib.auth.models import User
from django.db import models
from main.models.ya_market.order.choices import StatusChoices, PaymentTypeChoices, PriceTypeChoices, \
    ItemStatusChoices, StockTypeChoices, TypeOfPaymentChoices, PaymentSourseChoices, CommissionTypeChoices


class DeliveryRegion(models.Model):
    """
    Регионы доставки
    """
    region_id = models.PositiveIntegerField(verbose_name='Идентификатор региона доставки', null=True)
    name = models.CharField(max_length=255, verbose_name='Название региона доставки', null=True)


class Order(models.Model):
    """
    Заказы
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Пользователь")

    order_id = models.PositiveIntegerField(verbose_name='Идентификатор заказа')
    creationDate = models.DateField(
        verbose_name='Дата создания заказа',
        help_text='Формат даты: ГГГГ‑ММ‑ДД',
        null=True
    )
    status = models.CharField(
        max_length=27,
        choices=StatusChoices.choices,
        verbose_name='Текущий статус заказа',
        null=True
    )
    statusUpdateDate = models.DateTimeField(
        verbose_name='Дата и время, когда статус заказа был изменен в последний раз',
        help_text='Формат даты и времени: ISO 8601. '
                  'Например, 2017-11-21T00:00:00. Часовой пояс — UTC+03:00 (Москва)',
        null=True
    )
    paymentType = models.CharField(
        max_length=8,
        choices=PaymentTypeChoices.choices,
        verbose_name='Тип оплаты заказа',
        null=True
    )
    partnerOrderId = models.PositiveIntegerField(verbose_name='Идентификатор заказа партнера', null=True)
    deliveryRegion = models.ForeignKey(
        to=DeliveryRegion,
        on_delete=models.SET_NULL,
        verbose_name='Информация о регионе доставки',
        null=True
    )


class Warehouse(models.Model):
    """
    Cклады, на которых хранится товар
    """
    warehouse_id = models.PositiveIntegerField(verbose_name='Идентификатор склада', null=True)
    name = models.CharField(max_length=255, verbose_name='Название склада', null=True)


class Item(models.Model):
    """
    Информация о товаре в заказе после возможных изменений.
    """
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Список товаров в заказе после возможных изменений',
        help_text='В ходе обработки заказа Маркет может удалить из него единицы товаров — '
                  'при проблемах на складе или по инициативе пользователя. '
                  'Если из заказа удалены все единицы товара, его не будет в списке items — '
                  'только в списке initialItems. '
                  'Если в заказе осталась хотя бы одна единица товара, он будет и в списке items '
                  '(с уменьшенным количеством единиц count), '
                  'и в списке initialItems (с первоначальным количеством единиц initialCount).',
        null=True
    )
    offerName = models.CharField(max_length=255, verbose_name='Название товара', null=True)
    marketSku = models.PositiveIntegerField(verbose_name='SKU на Яндексе', null=True)
    shopSku = models.CharField(max_length=255, verbose_name='SKU товара в нашем магазине', null=True)
    count = models.PositiveIntegerField(
        verbose_name='Количество единиц товара с учетом удаленных единиц',
        help_text='Если из заказа удалены все единицы товара, он попадет только в список initialItems.',
        null=True
    )
    warehouse = models.ForeignKey(
        to=Warehouse,
        on_delete=models.SET_NULL,
        verbose_name='Информация о складе, на котором хранится товар',
        null=True
    )


class ItemPrice(models.Model):
    """
    Информация о цене или скидке на товар.
    """
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        related_name='prices',
        verbose_name='Цена или скидки на товар',
        null=True
    )
    type = models.CharField(
        max_length=11,
        choices=PriceTypeChoices.choices,
        verbose_name='Тип скидки или цена на товар',
        null=True
    )
    costPerItem = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена или скидка на единицу товара в заказе',
        help_text='Указана в рублях. Точность — два знака после запятой',
        null=True)
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Суммарная цена или скидка на все единицы товара в заказе',
        help_text='Указана в рублях. Точность — два знака после запятой',
        null=True)


class Detail(models.Model):
    """
    Информация о возврате товара или его неоплате при оформлении заказа
    """
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name='Информация об удалении товара из заказа',
        null=True
    )
    itemStatus = models.CharField(
        max_length=8,
        choices=ItemStatusChoices.choices,
        verbose_name='Статус товара',
        null=True
    )
    itemCount = models.PositiveIntegerField(
        verbose_name='Количество товара со статусом, указанном в параметре itemStatus',
        null=True
    )
    updateDate = models.DateField(
        verbose_name='Дата, когда товар получил статус, указанный в параметре itemStatus',
        help_text='Формат даты: ГГГГ‑ММ‑ДД',
        null=True
    )
    stockType = models.CharField(
        max_length=6,
        choices=StockTypeChoices.choices,
        verbose_name='Тип товара',
        null=True
    )


class InitialItem(models.Model):
    """
    Информация о товаре в заказе до изменений
    """
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='initialItems',
        verbose_name='Список товаров в заказе до изменений',
        help_text='В ходе обработки заказа Маркет может удалить из него единицы товаров — '
                  'при проблемах на складе или по инициативе пользователя. '
                  'Если из заказа удалены все единицы товара, его не будет в списке items — '
                  'только в списке initialItems. '
                  'Если в заказе осталась хотя бы одна единица товара, он будет и в списке items '
                  '(с уменьшенным количеством единиц count), '
                  'и в списке initialItems (с первоначальным количеством единиц initialCount).',
        null=True
    )
    offerName = models.CharField(max_length=255, verbose_name='Название товара', null=True)
    marketSku = models.PositiveIntegerField(verbose_name='SKU на Яндексе', null=True)
    shopSku = models.CharField(max_length=255, verbose_name='SKU товара в нашем магазине', null=True)
    initialCount = models.PositiveIntegerField(verbose_name='Первоначальное количество единиц товара', null=True)


class Payment(models.Model):
    """
    Информация о денежном переводе по заказу
    """
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Информация о денежных переводах по заказу',
        null=True
    )
    payment_id = models.CharField(
        max_length=255,
        verbose_name='Идентификатор денежного перевода',
        null=True
    )
    date = models.DateField(
        verbose_name='Дата денежного перевода',
        help_text='Формат даты: ГГГГ‑ММ‑ДД',
        null=True
    )
    type = models.CharField(
        max_length=7,
        choices=TypeOfPaymentChoices.choices,
        verbose_name='Тип денежного перевода',
        null=True
    )
    source = models.CharField(
        max_length=11,
        choices=PaymentSourseChoices.choices,
        verbose_name='Способ денежного перевода',
        null=True
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма денежного перевода',
        help_text='Значение указывается в рублях независимо от способа денежного перевода. '
                  'Точность — два знака после запятой',
        null=True)


class PaymentOrder(models.Model):
    """
    Информация о платежном поручении
    """
    payment = models.OneToOneField(
        to=Payment,
        on_delete=models.CASCADE,
        related_name='paymentOrder',
        verbose_name='Информация о платежном поручении',
        null=True
    )
    payment_order_id = models.IntegerField(verbose_name='Номер платежного поручения', null=True)
    date = models.DateField(
        verbose_name='Дата платежного поручения',
        help_text='Формат даты: ГГГГ‑ММ‑ДД',
        null=True
    )


class Commission(models.Model):
    """
    Комиссия за заказ
    """
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='commissions',
        verbose_name='Информация о комиссиях за заказ',
        null=True
    )
    type = models.CharField(
        max_length=11,
        choices=CommissionTypeChoices.choices,
        verbose_name='Тип комиссии',
        null=True
    )
    actual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма комиссии в рублях, которая была выставлена в момент создания заказа '
                     'и которую нужно оплатить',
        help_text='Точность — два знака после запятой',
        null=True)
    predicted = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма комиссии в рублях, которая была бы выставлена, '
                     'если бы заказ был создан в момент формирования отчета по заказам',
        help_text='Точность — два знака после запятой',
        null=True)
