from django.db import models


class TimeUnitChoices(models.TextChoices):
    HOUR = 'HOUR', 'часы'
    DAY = 'DAY', 'дни'
    WEEK = 'WEEK', 'недели'
    MONTH = 'MONTH', 'месяцы'
    YEAR = 'YEAR', 'годы'


class AvailabilityChoices(models.TextChoices):
    ACTIVE = 'ACTIVE', 'поставки будут'
    INACTIVE = 'INACTIVE', 'поставок не будет: товар есть на складе, но вы больше не планируете его поставлять. ' \
                           'Через 60 дней после того, как товар закончится на складе, этот статус изменится на DELISTED'
    DELISTED = 'DELISTED', 'архив: товар закончился на складе, и его поставок больше не будет. ' \
                           'Если товар вернется на склад (например, покупатель вернет заказ), ' \
                           'этот статус изменится на INACTIVE.'


class SupplyScheduleDayChoices(models.TextChoices):
    MONDAY = 'MONDAY', 'понедельник'
    TUESDAY = 'TUESDAY', 'вторник'
    WEDNESDAY = 'WEDNESDAY', 'среда'
    THURSDAY = 'THURSDAY', 'четверг'
    FRIDAY = 'FRIDAY', 'пятница'
    SATURDAY = 'SATURDAY', 'суббота'
    SUNDAY = 'SUNDAY', 'воскресенье'


class ProcessingStateStatus(models.TextChoices):
    READY = 'READY', 'товар прошел модерацию. Чтобы разместить его на Маркете, установите для него цену ' \
                     'и создайте поставку на склад. Подробнее см. в разделе Загрузка каталога товаров, ' \
                     'а также в разделе "Как поставить товары на склад" Справки Маркета для моделей FBY, FBY+ и FBS'
    IN_WORK = 'IN_WORK', 'товар проходит модерацию. Это занимает несколько дней'
    NEED_CONTENT = 'NEED_CONTENT', 'для товара без SKU на Яндексе market_sku нужно найти карточку самостоятельно ' \
                                   '(через API или личный кабинет магазина) или создать ее, ' \
                                   'если товар еще не продается на Маркете'
    NEED_INFO = 'NEED_INFO', 'товар не прошел модерацию из-за ошибок или недостающих сведений в описании товара. ' \
                             'Информация о причинах отклонения возвращается в параметре notes'
    REJECTED = 'REJECTED', 'товар не прошел модерацию, так как Маркет не планирует размещать подобные товары'
    SUSPENDED = 'SUSPENDED', 'товар не прошел модерацию, так как Маркет пока не размещает подобные товары'
    OTHER = 'OTHER', 'товар не прошел модерацию по другой причине. ' \
                     'Обратитесь в службу поддержки или к вашему менеджеру'


class ProcessingStateNoteType(models.TextChoices):
    ASSORTMENT = 'ASSORTMENT', 'товар производится в разных вариантах. Каждый из них нужно описать как отдельный товар'
    CANCELLED = 'CANCELLED', 'товар отозван с модерации по вашей инициативе'
    CONFLICTING_INFORMATION = 'CONFLICTING_INFORMATION', 'вы предоставили потиворечивую информацию о товаре. ' \
                                                         'Параметры, которые нужно исправить, ' \
                                                         'указаны в параметре payload'
    DEPARTMENT_FROZEN = 'DEPARTMENT_FROZEN', 'правила размещения товаров в данной категории перерабатываются, ' \
                                             'поэтому товар пока не может пройти модерацию'
    INCORRECT_INFORMATION = 'INCORRECT_INFORMATION', 'информация о товаре, которую вы предоставили, противоречит ' \
                                                     'описанию от производителя. Параметры, которые нужно исправить, ' \
                                                     'указаны в параметре payload'
    LEGAL_CONFLICT = 'LEGAL_CONFLICT', 'товар не прошел модерацию по юридическим причинам. Например, он официально ' \
                                       'не продается в России или у вас нет разрешения на его продажу'
    NEED_CLASSIFICATION_INFORMATION = 'NEED_CLASSIFICATION_INFORMATION', \
                                      'информации о товаре, которую вы предоставили, не хватает, чтобы отнести его к категории. ' \
                                      'Проверьте, что правильно указали название, категорию, производителя и страны производства товара, ' \
                                      'а также URL изображений или страниц с описанием, по которым можно идентифицировать товар'
    NEED_INFORMATION = 'NEED_INFORMATION', 'товар раньше не продавался в России и пока не размещается на Маркете. ' \
                                           'Для него можно создать карточку'
    NEED_PICTURES = 'NEED_PICTURES', 'для идентификации товара нужны его изображения'
    NEED_VENDOR = 'NEED_VENDOR', 'неверно указан производитель товара'
    NO_CATEGORY = 'NO_CATEGORY', 'товары из указанной категории пока не размещаются на Маркете. ' \
                                 'Если категория появится, товар будет снова отправлен на модерацию'
    NO_KNOWLEDGE = 'NO_KNOWLEDGE', 'товары из указанной категории пока не размещаются на Маркете. ' \
                                   'Если категория появится, товар будет снова отправлен на модерацию'
    NO_PARAMETERS_IN_SHOP_TITLE = 'NO_PARAMETERS_IN_SHOP_TITLE', \
                                  'товар производится в разных вариантах, и из указанного названия непонятно, ' \
                                  'о каком идет речь. Параметры, которые нужно добавить в название товара, ' \
                                  'указаны в параметре payload'
    NO_SIZE_MEASURE = 'NO_SIZE_MEASURE', 'для этого товара нужна размерная сетка. Отправьте ее в службу поддержки ' \
                                         'или вашему менеджеру. Требования к размерной сетке ' \
                                         'указаны в параметре payload'
    UNKNOWN = 'UNKNOWN', 'товар не прошел модерацию по другой причине. ' \
                         'Обратитесь в службу поддержки или к вашему менеджеру'


class MappingType(models.TextChoices):
    BASE = 'BASE', 'Информация о текущей карточке товара на Маркете'
    AWAITING_MODERATION = 'AWAITING_MODERATION', 'Информация о карточке товара на Маркете, ' \
                                                 'проходящей модерацию для данного товара'
    REJECTED = 'REJECTED', 'Информация о последней карточке товара на Маркете, ' \
                           'отклоненной на модерации для данного товара'


class VatType(models.IntegerChoices):
    two = 2, '10 %'
    five = 5, '0 %'
    six = 6, 'не облагается'
    seven = 7, '20 %'

