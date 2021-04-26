"""Базовый класс для набора форм"""

import random
import string
from typing import List
from django.db import models
from django.forms import ModelForm
from rest_framework.utils import model_meta


class FormParser:
    """Парсер для одной формы из набора форм"""
    def __init__(self, base_form):
        self.base_form = base_form
        self.form: ModelForm
        self.attrs: dict = dict()

    def __template_request(self, disable: bool, model=None, attrs: dict = None, post=None):
        """Подготовка начальных данных для одной формы"""
        if model and attrs:
            self.attrs = attrs
            try:
                instance = model.objects.filter(**attrs)[0]
                self.form = self.base_form(post, instance=instance) if post \
                    else self.base_form(instance=instance)
            except IndexError:
                self.form = self.base_form(post) if post else self.base_form()
        else:
            self.form = self.base_form()
        self.form.turn_off(disable=disable)

    def fill(self, model: models.Model, attrs: dict, disable: bool) -> None:
        """передает аргументы для формы с заполнением"""
        self.__template_request(disable=disable, model=model, attrs=attrs)

    def clear(self, disable: bool) -> None:
        """передает аргументы для формы без заполнения"""
        self.__template_request(disable=disable)

    def post(self, post, model: models.Model, attrs: dict, disable: bool) -> None:
        """передает аргументы для формы с Post запросом"""
        self.__template_request(disable=disable, model=model, attrs=attrs, post=post)

    def __bool__(self):
        return self.form.is_valid()


class Multiform:
    """
    Класс-парсер для набора форм
    """
    def __init__(self):
        self.forms_model_list: List = []
        self.forms_dict: dict = {}

    @staticmethod
    def __random_id():
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(5))

    def context(self, accordions: List, forms: List[List]) -> dict:
        """Подготовка контекста из списка форм"""
        return dict(zip(accordions, [[self.__random_id(), form] for form in forms]))

    def __template_request(self, disable: bool, post=None, method: str = None,
                           attrs: bool = None, model: bool = None):
        """Подготовка начальных данных для всех форм"""
        for data in self.forms_model_list:
            form = FormParser(base_form=data['form'])
            attributes = {}
            if post:
                attributes.update({'post': post})
            if model:
                attributes.update({'model': data['form'].Meta.model})
            if attrs:
                attributes.update({'attrs': data['attrs']})
            getattr(form, method)(**attributes, disable=disable)
            self.forms_dict.update({str(data['form']()): form})

    def set_forms(self, pk) -> None:
        """Список форм (устанавливается индивидуально для каждой набора форм)"""
        raise NotImplementedError

    def set_post(self, disable: bool, post) -> None:
        """Вызывать для формы с POST запросом."""
        self.__template_request(model=True, attrs=True, post=post, method='post', disable=disable)

    def set_fill(self, disable: bool) -> None:
        """Вызывать для get запроса с учетом заполнения формы из модели."""
        self.__template_request(model=True, attrs=True, method='fill', disable=disable)

    def set_clear(self, disable: bool) -> None:
        """Вызывать для get запроса без заполнения данными из модели (возвращает пустые поля)."""
        self.__template_request(method='clear', disable=disable)

    def get_form_list(self, forms: list) -> list:
        """Возвращает формы из списка форм (в нем лежат их классы)."""
        return [self.forms_dict[str(form())].form for form in forms]

    def get_for_context(self) -> dict:
        """Подготовка контекста из списка форм (индивидуально для каждой набора форм)."""
        raise NotImplementedError

    def is_valid(self) -> bool:
        """Проверка валидности всех вложенных моделей."""
        for key, form in self.forms_dict.items():
            if not form:
                return False
        return True

    def save(self) -> None:
        """Сохранение всех форм, если они не пустые."""
        for key, form_parser in self.forms_dict.items():
            if form_parser.form.is_valid():
                print(form_parser.form)
                instance = form_parser.form.save(commit=False)
                if not_empty(instance):
                    for field in form_parser.attrs.keys():
                        setattr(instance, field, form_parser.attrs[field])
                    instance.save()
                    """удаляем сохраненный объект, если он стал пустым"""
                    if not not_empty(instance, exclude_forwards=True):
                        instance.delete()


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
