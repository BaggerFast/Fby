"""Базовый класс для набора форм"""

import random
import string
from typing import List
from django.db import models
from django.forms import ModelForm
from rest_framework.utils import model_meta


class Multiform:
    """
    Класс-парсер для набора форм
    """
    def __init__(self):
        self.forms_dict: dict = {}

    def get_form_list(self, form_list) -> list:
        """Возвращает формы из списка форм (в нем лежат их классы)."""
        return [self.forms_dict[form] for form in form_list]

    @staticmethod
    def __random_id():
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(5))

    def context(self, accordions, forms_context) -> dict:
        """Подготовка контекста из списка форм"""
        return dict(zip(accordions, [[self.__random_id(), form] for form in forms_context]))

    def get_for_context(self):
        pass

    def is_valid(self) -> bool:
        """Проверка валидности всех вложенных моделей."""
        for key, form in self.forms_dict.items():
            if not form:
                return False
        return True

