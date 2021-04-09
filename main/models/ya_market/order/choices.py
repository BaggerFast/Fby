from django.db import models


class StatusChoices(models.TextChoices):
    CANCELLED_BEFORE_PROCESSING = 'CANCELLED_BEFORE_PROCESSING', 'заказ отменен до начала его обработки'
    CANCELLED_IN_DELIVERY = 'CANCELLED_IN_DELIVERY', 'заказ отменен во время его доставки'
    CANCELLED_IN_PROCESSING = 'CANCELLED_IN_PROCESSING', 'заказ отменен во время его обработки'
    DELIVERY = 'DELIVERY', 'заказ передан службе доставки'
    DELIVERED = 'DELIVERED', 'заказ доставлен'
    PARTIALLY_RETURNED = 'PARTIALLY_RETURNED', 'заказ частично возвращен покупателем'
    PICKUP = 'PICKUP', 'заказ доставлен в пункт выдачи'
    PROCESSING = 'PROCESSING', 'заказ в обработке'
    REJECTED = 'REJECTED', 'заказ создан, но не оплачен'
    RETURNED = 'RETURNED', 'заказ полностью возвращен покупателем'
    UNKNOWN = 'UNKNOWN', 'неизвестный статус заказа'


class PaymentTypeChoices(models.TextChoices):
    CREDIT = 'CREDIT', 'заказ оформлен в кредит'
    POSTPAID = 'POSTPAID', 'заказ оплачен после того, как был получен'
    PREPAID = 'PREPAID', 'заказ оплачен до того, как был получен'


class PriceTypeChoices(models.TextChoices):
    BUYER = 'BUYER', 'цена на товар с учетом скидок, в том числе Маркет Бонусов и бонусов СберСпасибо'
    CASHBACK = 'CASHBACK', 'баллы кешбэка по подписке Яндекс Плюс'
    MARKETPLACE = 'MARKETPLACE', 'Маркет Бонусы'
    SPASIBO = 'SPASIBO', 'бонусы СберСпасибо'


class ItemStatusChoices(models.TextChoices):
    REJECTED = 'REJECTED', 'товар был добавлен в созданный заказ, но не был оплачен'
    RETURNED = 'RETURNED', 'товар вернули'


class StockTypeChoices(models.TextChoices):
    DEFECT = 'DEFECT', 'товар бракованный'
    FIT = 'FIT', 'товар надлежащего качества'


class TypeOfPaymentChoices(models.TextChoices):
    PAYMENT = 'PAYMENT', 'оплата'
    REFUND = 'REFUND', 'возврат'


class PaymentSourseChoices(models.TextChoices):
    BUYER = 'BUYER', 'оплата или возврат деньгами'
    CASHBACK = 'CASHBACK', 'оплата или возврат баллами кешбэка по подписке Яндекс Плюс'
    MARKETPLACE = 'MARKETPLACE', 'оплата или возврат Маркет Бонусами'
    SPASIBO = 'SPASIBO', 'оплата или возврат бонусами СберСпасибо'


class CommissionTypeChoices(models.TextChoices):
    AGENCY = 'AGENCY', 'прием и перечисление денег от покупателя (агентское вознаграждение)'
    FEE = 'FEE', 'комиссия за размещение товара на Маркете'
    FULFILLMENT = 'FULFILLMENT', 'комиссия за хранение товара на складе Маркета'
