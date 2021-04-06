import random
import string
from pprint import pprint
from typing import List


class FormParser:
    def __init__(self, base_form):
        self.form_base = base_form
        self.form = None

    @staticmethod
    def __get_or_create(model, attrs_for_filter):
        try:
            model = model.objects.filter(**attrs_for_filter)[0]
        except IndexError:
            model = model.objects.create(**attrs_for_filter)
        return model

    def __template_request(self, disable: bool, model=None, attrs_for_filter=None, request=None):
        if model and attrs_for_filter:
            model = self.__get_or_create(model=model, attrs_for_filter=attrs_for_filter)
            self.form = self.form_base(request, instance=model) if request else self.form_base(instance=model)
        else:
            self.form = self.form_base()
        self.form.turn_off(disable=disable)

    def fill(self, model, attrs_for_filter, disable) -> None:
        self.__template_request(disable=disable, model=model, attrs_for_filter=attrs_for_filter)

    def clear(self, disable) -> None:
        self.__template_request(disable=disable)

    def post(self, request, model, attrs_for_filter, disable) -> None:
        self.__template_request(disable=disable, model=model, attrs_for_filter=attrs_for_filter, request=request)

    def __bool__(self):
        return self.form.is_valid()


class Multiform:
    def __init__(self):
        self.model_list = None
        self.models_json = {}

    @staticmethod
    def random_id():
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(5))

    def context(self, names: list, forms: List[List]) -> dict:
        return dict(zip(names, [[self.random_id(), form] for form in forms]))

    def __template_request(self, disable: bool, request=None, method=None, attrs_for_filter=None, model: str = None):
        self.models_json.clear()
        for cur_model in self.model_list:
            form = FormParser(base_form=cur_model['form'])
            json = {}
            if request:
                json.update({'request': request})
            if model:
                json.update({'model': cur_model['form'].Meta.model})
            if attrs_for_filter:
                json.update({'attrs_for_filter': cur_model['attrs']})
            getattr(form, method)(**json, disable=disable)
            self.models_json.update({str(cur_model['form']()): form})

    def get_models_classes(self) -> None:
        # примеры смотрите в коде
        raise NotImplementedError

    def get_post(self, disable: bool, request) -> None:
        json = {'model': True, 'attrs_for_filter': True, 'request': request, 'method': 'post', 'disable': disable}
        self.__template_request(**json)

    def get_fill(self, disable: bool) -> None:
        # вызывать для get запроса с учетом заполнения формы из модели
        json = {'model': True, 'attrs_for_filter': True, 'method': 'fill', 'disable': disable}
        self.__template_request(**json)

    def get_clear(self, disable: bool) -> None:
        # вызывать для get запроса без заполнения данными из модели (возвращает пустые поля)
        json = {'method': 'clear', 'disable': disable}
        self.__template_request(**json)

    def get_form_list(self, forms: list) -> list:
        return [self.models_json[str(form())].form for form in forms]

    def get_for_context(self) -> dict:
        # примеры смотрите в коде
        raise NotImplementedError

    def is_valid(self) -> bool:
        # проверяет формы на валидность
        for key, model in self.models_json.items():
            if not model:
                return False
        return True

    def save(self) -> None:
        # сохраняет все формы
        for key, model in self.models_json.items():
            model.form.save()

