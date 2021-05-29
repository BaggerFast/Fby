from dataclasses import dataclass
from typing import List, Dict, Union
from django.urls import reverse


class Navbar:
    @dataclass
    class __Nested:
        url: str
        label: str
        active: bool = False

    @dataclass
    class __Field:
        label: str
        nested_fields: list

    def __init__(self, request):
        self.__request = request
        self.__nav = []

    def __off_current(self):
        for menu_item in self.__nav:
            if type(menu_item) == self.__Field:
                # для атрибута меню с выпадающим списком
                for i in range(len(menu_item.nested_fields)):
                    menu_item.nested_fields[i].active = self.__request.path != reverse(menu_item.nested_fields[i].url)
            else:
                # для обычных атрибутов
                menu_item.active = self.__request.path != reverse(menu_item.url)

    def __static_point(self):
        return [self.__Nested(url='index', label='Главная')]

    def __auth_point(self):
        if self.__request.user.is_authenticated:
            self.__nav += [
                self.__Field(label='Товары', nested_fields=[self.__Nested(url='catalogue_offer', label="Каталог"),
                                                            self.__Nested(url='create_offer', label="Создать")]),
                self.__Field(label='Заказы', nested_fields=[self.__Nested(url='catalogue_order', label="Каталог"),
                                                            self.__Nested(url='summary', label='Отчёт')])
            ]

    def __not_auth_point(self):
        if not self.__request.user.is_authenticated:
            self.__nav += [
                self.__Field(label='Авторизация', nested_fields=[
                    self.__Nested(url='login', label='Войти'),
                    self.__Nested(url='register', label='Зарегистрироваться')])
            ]

    def __user_point(self):
        return [self.__Nested(url='logout', label="Выйти"), self.__Nested(url='profile', label="Личный кабинет")]

    def get(self) -> Dict:
        """
        возвращает аттрибуты для меню
        """
        self.__not_auth_point()
        self.__auth_point()
        self.__static_point()
        self.__off_current()
        return {'main': self.__nav, 'user': self.__user_point()}
