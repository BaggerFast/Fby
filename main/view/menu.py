from typing import List, Dict, Union

from django.urls import reverse


def get_navbar(request) -> Dict[str, Union[list, List[Dict[str, str]]]]:

    def off_current(nav: List):
        for menu_item in nav:
            if menu_item.get('list', False):
                # для атрибута меню с выпадающим списком
                for i in range(len(menu_item['list'])):
                    menu_item['list'][i]['active'] = request.path != reverse(menu_item['list'][i]['url'])
            else:
                # для обычных атрибутов
                menu_item['active'] = request.path != reverse(menu_item['url'])
        return nav

    def static_point():
        return [
            {'url': 'index', 'label': 'Главная'}
        ]

    def auth_point(nav: List):
        if request.user.is_authenticated:
            nav += [
                {'label': 'Товары', 'list': [{'url': 'catalogue_list', 'label': "Каталог"},
                                             {'url': 'create_offer', 'label': "Создать"}]},
                {'label': 'Заказы', 'url': 'orders_list'}
            ]
        return nav

    def not_auth_point(nav: List):
        if not request.user.is_authenticated:
            nav += [
                {'label': 'Авторизация', 'list': [
                    {'url': 'login', 'label': 'Войти'},
                    {'url': 'register', 'label': 'Зарегистрироваться'}
                ]}
            ]
        return nav

    def user_point():
        return [{'url': 'logout', 'label': "Выйти"}, {'url': 'profile', 'label': "Личный кабинет"}]
    """
    возвращает атрибутты для меню
    """
    data = {'main': off_current(not_auth_point(auth_point(static_point()))), 'user': user_point()}
    return data
