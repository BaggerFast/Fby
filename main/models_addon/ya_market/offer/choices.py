"""Choices для моделей из Offer"""

from django.db import models


class PriceSuggestionChoices(models.TextChoices):
    BUYBOX = "BUYBOX", "Минимальная цена у партнеров на Маркете."

    DEFAULT_OFFER = "DEFAULT_OFFER", "Рекомендованная Маркетом цена, которая привлекает покупателей."

    MIN_PRICE_MARKET = "MIN_PRICE_MARKET", "Минимальная цена на Маркете"

    MAX_DISCOUNT_BASE = "MAX_DISCOUNT_BASE", "Максимальная цена товара без скидки"

    MARKET_OUTLIER_PRICE = "MARKET_OUTLIER_PRICE", "Максимальная цена товара, которая обеспечивает показы на Маркете."


class TimeUnitChoices(models.TextChoices):
    """
    Единицы времени.
    """
    HOUR = 'HOUR', 'часы'
    DAY = 'DAY', 'дни'
    WEEK = 'WEEK', 'недели'
    MONTH = 'MONTH', 'месяцы'
    YEAR = 'YEAR', 'годы'


class AvailabilityChoices(models.TextChoices):
    """
    Доступен ли товар.
    """
    ACTIVE = 'ACTIVE', 'Поставки будут'
    INACTIVE = 'INACTIVE', 'Поставок не будет: товар есть на складе, но вы больше не планируете его поставлять.'
    DELISTED = 'DELISTED', 'Архив: товар закончился на складе, и его поставок больше не будет.'


class SupplyScheduleDayChoices(models.TextChoices):
    """
    Дни недели.
    """
    MONDAY = 'MONDAY', 'понедельник'
    TUESDAY = 'TUESDAY', 'вторник'
    WEDNESDAY = 'WEDNESDAY', 'среда'
    THURSDAY = 'THURSDAY', 'четверг'
    FRIDAY = 'FRIDAY', 'пятница'
    SATURDAY = 'SATURDAY', 'суббота'
    SUNDAY = 'SUNDAY', 'воскресенье'


class ProcessingStateStatus(models.TextChoices):
    """
    Статус модерации товара.
    """
    READY = 'READY', """товар прошел модерацию. Чтобы разместить его на Маркете, установите для него цену и 
                        создайте поставку на склад."""

    IN_WORK = 'IN_WORK', 'Товар проходит модерацию. Может занять несколько дней'

    NEED_CONTENT = 'NEED_CONTENT', 'для товара без SKU на Яндексе market_sku нужно найти карточку самостоятельно'

    NEED_INFO = 'NEED_INFO', 'Товар не прошел модерацию из-за ошибок или недостающих сведений в описании товара.'

    REJECTED = 'REJECTED', 'Товар не прошел модерацию, так как Маркет не планирует размещать подобные товары'

    SUSPENDED = 'SUSPENDED', 'Товар не прошел модерацию, так как Маркет пока не размещает подобные товары'

    OTHER = 'OTHER', 'товар не прошел модерацию по другой причине. Обратитесь в службу поддержки или к вашему менеджеру'


class ProcessingStateNoteType(models.TextChoices):
    """
    Причина по которой товар не прошёл модерацию.
    """
    ASSORTMENT = 'ASSORTMENT', 'Товар производится в разных вариантах. Каждый из них нужно описать как отдельный товар'

    CANCELLED = 'CANCELLED', 'Товар отозван с модерации по вашей инициативе'

    CONFLICTING_INFORMATION = 'CONFLICTING_INFORMATION', 'Вы предоставили противоречивую информацию о товаре.'

    DEPARTMENT_FROZEN = 'DEPARTMENT_FROZEN', 'Правила размещения товаров в данной категории перерабатываются,'

    INCORRECT_INFORMATION = 'INCORRECT_INFORMATION', """Информация о товаре, которую вы предоставили, противоречит'
                                                        описанию от производителя."""

    LEGAL_CONFLICT = 'LEGAL_CONFLICT', 'товар не прошел модерацию по юридическим причинам.'

    NEED_CLASSIFICATION_INFORMATION = 'NEED_CLASSIFICATION_INFORMATION', """Информации о товаре, которую вы 
                                            предоставили, не хватает, чтобы отнести его к категории"""

    NEED_INFORMATION = 'NEED_INFORMATION', 'Товар раньше не продавался в России и пока не размещается на Маркете.'

    NEED_PICTURES = 'NEED_PICTURES', 'Для идентификации товара нужны его изображения'

    NEED_VENDOR = 'NEED_VENDOR', 'Неверно указан производитель товара'

    NO_CATEGORY = 'NO_CATEGORY', 'Товары из указанной категории пока не размещаются на Маркете.'

    NO_KNOWLEDGE = 'NO_KNOWLEDGE', ''

    NO_PARAMETERS_IN_SHOP_TITLE = 'NO_PARAMETERS_IN_SHOP_TITLE', 'товар производится в разных вариантах, и из ' \
                                                                 'указанного названия непонятно, о каком идет речь.'

    NO_SIZE_MEASURE = 'NO_SIZE_MEASURE', 'для этого товара нужна размерная сетка. Отправьте ее в службу поддержки'

    UNKNOWN = 'UNKNOWN', 'товар не прошел модерацию по другой причине. Обратитесь в службу поддержки или к вашему' \
                         ' менеджеру'


class MappingType(models.TextChoices):
    """
    Тип маппинга товара.
    """
    BASE = 'BASE', 'Информация о текущей карточке товара на Маркете'
    AWAITING_MODERATION = 'AWAITING_MODERATION', 'Информация о карточке товара на Маркете, ' \
                                                 'проходящей модерацию для данного товара'
    REJECTED = 'REJECTED', 'Информация о последней карточке товара на Маркете, ' \
                           'отклоненной на модерации для данного товара'


class VatType(models.IntegerChoices):
    """
    НДС товара.
    """
    two = 2, '10 %'
    five = 5, '0 %'
    six = 6, 'не облагается'
    seven = 7, '20 %'


class CurrencyChoices(models.TextChoices):
    RUR = 'RUR', 'Руб.'
