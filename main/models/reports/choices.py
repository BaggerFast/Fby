from django.db import models


class StockTypeChoices(models.TextChoices):
    AVAILABLE = 'AVAILABLE', 'Товар, доступный для продажи'
    DEFECT = 'DEFECT', 'Товар с браком'
    EXPIRED = 'EXPIRED', 'Товар с истекшим сроком годности'
    FIT = 'FIT', 'Товар, который доступен для продажи или уже зарезервирован'
    FREEZE = 'FREEZE', 'Товар, который зарезервирован для заказов'
    QUARANTINE = 'QUARANTINE', 'Товар, временно недоступный для продажи (например, товар перемещают из одного ' \
                               'помещения склада в другое) '
    UTILIZATION = 'UTILIZATION', 'Товар, который будет утилизирован'
    SUGGEST = 'SUGGEST', 'Товар, который рекомендуется поставить на склад (могут заказать в ближайшие две недели)'
    TRANSIT = 'TRANSIT', 'Проданный товар'


class StorageTypeChoices(models.TextChoices):
    FREE = 'FREE', 'Товар, который хранится на складе бесплатно'
    PAID = 'PAID', 'Товар, который хранится платно по обычному тарифу'


class InclusionTypeChoices(models.TextChoices):
    FREE_EXPIRE = 'FREE_EXPIRE', 'Товар,  у которого срок бесплатного хранения подходит к концу. Значение ' \
                                 'возвращается для товаров с типом условий хранения и обработки FREE'
    PAID_EXPIRE = 'PAID_EXPIRE', 'Товар, за хранение которого скоро придется платить по повышенному тарифу. Значение ' \
                                 'возвращается для товаров с типом условий хранения и обработки PAID'
    PAID_EXTRA = 'PAID_EXTRA', 'Товар, который хранится платно по повышенному тарифу. Значение возвращается для ' \
                               'товаров с типом условий хранения и обработки PAID'


class TariffTypeChoices(models.TextChoices):
    AGENCY_COMMISSION = 'AGENCY_COMMISSION', 'Прием и перечисление денег от покупателя (агентское вознаграждение)'
    FULFILLMENT = 'FULFILLMENT ', 'Обработка товара на складе Маркета'
    STORAGE = 'STORAGE', 'Хранение товара на складе Маркета в течение суток'
    SURPLUS = 'SURPLUS', 'Хранение излишков на складе Маркета'
    WITHDRAW = 'WITHDRAW', 'Вывоз товара со склада Маркета'
    FEE = 'FEE', 'Размещение товара на Маркете'
