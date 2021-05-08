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
    forms_dict: dict = {}
    forms: dict = {}

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
        raise NotImplementedError

    def is_valid(self) -> bool:
        """Проверка валидности всех вложенных моделей."""
        for form in self.forms_dict.values():
            if not form:
                return False
        return True

    def set_disable(self, disable=False):
        for form in self.forms_dict.values():
            form.turn_off(disable)

    def get_fill(self):
        for attrs in self.forms:
            self.forms_dict.update({attrs[0]: attrs[0](instance=attrs[1])})

    def get_space(self):
        for attrs in self.forms:
            self.forms_dict.update({attrs[0]: attrs[0]()})

    def set_post(self, post):
        for attrs in self.forms:
            self.forms_dict.update({attrs[0]: attrs[0](post, instance=attrs[1])})

    def write_foreign_key(self, instance):
        return instance

    def save(self) -> None:
        """Сохранение всех форм, если они не пустые."""
        for form in self.forms_dict.values():
            if form.is_valid():
                instance = self.write_foreign_key(form.save(commit=False))
                if self.not_empty(instance):
                    instance.save()
                    """удаляем сохраненный объект, если он стал пустым"""
                    if not self.not_empty(instance, exclude_forwards=True):
                        instance.delete()

    @staticmethod
    def not_empty(instance, exclude_forwards: bool = False) -> bool:
        """Проверяет, что объект не пустой.
        Если среди всех полей объекта, есть хотя бы одно непустое, возвращает True, иначе - False
        Если параметр exclude_forwards=True, то из поиска исключаются поля forward_relations
        """
        model = instance._meta.model
        fields = instance._meta.fields
        forward_fields = [field for field in model_meta.get_field_info(model).forward_relations]
        if exclude_forwards:
            fields = [field for field in fields if field.name not in forward_fields]
        for field in fields:
            if field.name != 'id' and getattr(instance, field.name, None):
                return True
        return False
