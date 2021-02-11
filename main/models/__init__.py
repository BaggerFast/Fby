"""
Основные модели проекта.

Сформированы на основе API Яндекс.Маркета (FBY)

.. sectionauthor:: Andrew Smirnov <smirnov@informatics.ru>
.. codeauthor:: Andrew Smirnov <smirnov@informatics.ru>
.. seealso::
   https://yandex.ru/dev/market/partner-marketplace/doc/dg/reference/get-campaigns-id-offer-mapping-entries.html
.. todo::
   Установить значения по умолчанию везде, где это возможно
.. todo::
   Добавить документацию для ENUM'ов
.. todo::
   Добавить сериализаторы для каждой модели (с трансляцией имён в формат Яндекса и обратно)
"""

from .choices import *
from .support import *
from .base import *
