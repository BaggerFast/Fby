"""Choices для моделей из Reports"""

from django.db import models


class StockTypeChoices(models.TextChoices):
    """
    Тип товара.
    """
    AVAILABLE = 'AVAILABLE', 'Товар, доступный для продажи'
    DEFECT = 'DEFECT', 'Товар с браком'
    EXPIRED = 'EXPIRED', 'Товар с истекшим сроком годности'
    FIT = 'FIT', 'Товар, который доступен для продажи или уже зарезервирован'
    FREEZE = 'FREEZE', 'Товар, который зарезервирован для заказов'
    QUARANTINE = 'QUARANTINE', 'Товар, временно недоступный для продажи'
    UTILIZATION = 'UTILIZATION', 'Товар, который будет утилизирован'
    SUGGEST = 'SUGGEST', 'Товар, который рекомендуется поставить на склад'
    TRANSIT = 'TRANSIT', 'Проданный товар'


class StorageTypeChoices(models.TextChoices):
    """
    Типы хранения товара.
    """
    FREE = 'FREE', 'Товар, который хранится на складе бесплатно'
    PAID = 'PAID', 'Товар, который хранится платно по обычному тарифу'


class InclusionTypeChoices(models.TextChoices):
    """
    Типы оплаты хранения товара.
    """
    FREE_EXPIRE = 'FREE_EXPIRE', 'Товар,  у которого срок бесплатного хранения подходит к концу.'
    PAID_EXPIRE = 'PAID_EXPIRE', 'Товар, за хранение которого скоро придется платить по повышенному тарифу.'
    PAID_EXTRA = 'PAID_EXTRA', 'Товар, который хранится платно по повышенному тарифу.'


class TariffTypeChoices(models.TextChoices):
    """
    Типы тарифов.
    """
    AGENCY_COMMISSION = 'AGENCY_COMMISSION', 'Прием и перечисление денег от покупателя (агентское вознаграждение)'
    FULFILLMENT = 'FULFILLMENT', 'Обработка товара на складе Маркета'
    STORAGE = 'STORAGE', 'Хранение товара на складе Маркета в течение суток'
    SURPLUS = 'SURPLUS', 'Хранение излишков на складе Маркета'
    WITHDRAW = 'WITHDRAW', 'Вывоз товара со склада Маркета'
    FEE = 'FEE', 'Размещение товара на Маркете'
