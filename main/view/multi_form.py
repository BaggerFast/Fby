import random
import string
from typing import List
from django.db import models
from django.forms import ModelForm


class FormParser:
    def __init__(self, base_form):
        self.base_form = base_form
        self.form: ModelForm

    @staticmethod
    def __get_or_create(model: models.Model, attrs_for_filter: dict) -> models.Model:
        try:
            return model.objects.filter(**attrs_for_filter).first()
        except IndexError:
            return model.objects.create(**attrs_for_filter)

    def __template_request(self, disable: bool, model=None, attrs_for_filter: dict = None, post=None):
        if model and attrs_for_filter:
            model = self.__get_or_create(model=model, attrs_for_filter=attrs_for_filter)
            print(model)
            self.form = self.base_form(post, instance=model) if post else self.base_form(instance=model)
        else:
            self.form = self.base_form()
        self.form.turn_off(disable=disable)

    def fill(self, model: models.Model, attrs_for_filter: dict, disable: bool) -> None:
        # передает аргументы для формы с заполнением
        self.__template_request(disable=disable, model=model, attrs_for_filter=attrs_for_filter)

    def clear(self, disable: bool) -> None:
        # передает аргументы для формы без заполнения
        self.__template_request(disable=disable)

    def post(self, post, model: models.Model, attrs_for_filter: dict, disable: bool) -> None:
        # передает аргументы для формы с Post запросом
        self.__template_request(disable=disable, model=model, attrs_for_filter=attrs_for_filter, post=post)

    def __bool__(self):
        return self.form.is_valid()


class Multiform:
    def __init__(self):
        self.forms_model_list: List = []
        self.forms_dict: dict = {}

    @staticmethod
    def __random_id():
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(5))

    def context(self, accordions: List, forms: List[List]) -> dict:
        return dict(zip(accordions, [[self.__random_id(), form] for form in forms]))

    def __template_request(self, disable: bool, post=None, method: str = None, attrs: bool = None, model: bool = None):
        for cur_model in self.forms_model_list:
            form = FormParser(base_form=cur_model['form'])
            attributes = {}
            if post:
                attributes.update({'post': post})
            if model:
                attributes.update({'model': cur_model['form'].Meta.model})
            if attrs:
                attributes.update({'attrs_for_filter': cur_model['attrs']})
            getattr(form, method)(**attributes, disable=disable)
            self.forms_dict.update({str(cur_model['form']()): form})

    def set_forms(self) -> None:
        # примеры смотрите в коде
        raise NotImplementedError

    def set_post(self, disable: bool, request) -> None:
        # вызывать для формы с POST запросом
        self.__template_request(model=True, attrs=True, post=request, method='post', disable=disable)

    def set_fill(self, disable: bool) -> None:
        # вызывать для get запроса с учетом заполнения формы из модели
        self.__template_request(model=True, attrs=True, method='fill', disable=disable)

    def set_clear(self, disable: bool) -> None:
        # вызывать для get запроса без заполнения данными из модели (возвращает пустые поля)
        self.__template_request(method='clear', disable=disable)

    def get_form_list(self, forms: list) -> list:
        # возращает формы из списка форм (в нем лежат их классы)
        return [self.forms_dict[str(form())].form for form in forms]

    def get_for_context(self) -> dict:
        # примеры смотрите в коде
        raise NotImplementedError

    def is_valid(self) -> bool:
        """
        Проверка валидности всех вложенных моделей
        """
        for key, model in self.forms_dict.items():
            if not model:
                return False
        return True

    def save(self) -> None:
        # сохраняет все формы
        for key, form_parser in self.forms_dict.items():
            form_parser.form.save()
