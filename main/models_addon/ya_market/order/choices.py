"""Choices для моделей из Order"""

from django.db import models


class StatusChoices(models.TextChoices):
    CANCELLED_BEFORE_PROCESSING = 'CANCELLED_BEFORE_PROCESSING', 'Отменён до обработки'
    CANCELLED_IN_DELIVERY = 'CANCELLED_IN_DELIVERY', 'Отменен во время его доставки'
    CANCELLED_IN_PROCESSING = 'CANCELLED_IN_PROCESSING', 'Отменен во время его обработки'
    DELIVERY = 'DELIVERY', 'Передан службе доставки'
    DELIVERED = 'DELIVERED', 'Доставлен'
    PARTIALLY_RETURNED = 'PARTIALLY_RETURNED', 'Частично возвращен покупателем'
    PICKUP = 'PICKUP', 'Доставлен в пункт выдачи'
    PROCESSING = 'PROCESSING', 'В обработке'
    REJECTED = 'REJECTED', 'Создан, но не оплачен'
    RETURNED = 'RETURNED', 'Полностью возвращен покупателем'
    UNKNOWN = 'UNKNOWN', 'Неизвестный статус'


class PaymentTypeChoices(models.TextChoices):
    CREDIT = 'CREDIT', 'Оформлен в кредит'
    POSTPAID = 'POSTPAID', 'Оплачен после получения'
    PREPAID = 'PREPAID', 'Оплачен до получения'


class PriceTypeChoices(models.TextChoices):
    BUYER = 'BUYER', 'Цена на товар с учетом скидок'
    CASHBACK = 'CASHBACK', 'Скидка по баллам Яндекс Плюс за шт.'
    MARKETPLACE = 'MARKETPLACE', 'Скидка по бонусам Маркета за шт.'
    SPASIBO = 'SPASIBO', 'Скидка по бонусам СберСпасибо за шт.'


class ItemStatusChoices(models.TextChoices):
    REJECTED = 'REJECTED', 'товар был добавлен в созданный заказ, но не был оплачен'
    RETURNED = 'RETURNED', 'товар вернули'


class StockTypeChoices(models.TextChoices):
    DEFECT = 'DEFECT', 'товар бракованный'
    FIT = 'FIT', 'товар надлежащего качества'


class TypeOfPaymentChoices(models.TextChoices):
    PAYMENT = 'PAYMENT', 'Платеж'
    REFUND = 'REFUND', 'Возврат платежа'


class PaymentSourceChoices(models.TextChoices):
    BUYER = 'BUYER', 'покупателя'
    CASHBACK = 'CASHBACK', 'за скидку по баллам Яндекс.Плюса'
    MARKETPLACE = 'MARKETPLACE', 'за скидку маркетплейса'
    SPASIBO = 'SPASIBO', 'за скидку по бонусам СберСпасибо'


class CommissionTypeChoices(models.TextChoices):
    AGENCY = 'AGENCY', 'прием и перечисление денег от покупателя (агентское вознаграждение)'
    FEE = 'FEE', 'комиссия за размещение товара на Маркете'
    FULFILLMENT = 'FULFILLMENT', 'комиссия за хранение товара на складе Маркета'
