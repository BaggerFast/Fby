from django.urls import reverse


def get_navbar(request) -> list:
    def off_current(nav: list, req):
        for menu_item in nav:
            if menu_item.get('list', False):
                # для атрибута меню с выпадающим списком
                for i in range(len(menu_item['list'])):
                    menu_item['list'][i]['active'] = req.path != reverse(menu_item['list'][i]['url'])
            else:
                # для обычных атрибутов
                menu_item['active'] = req.path != reverse(menu_item['url'])
        return nav

    """
    возвращает атрибутты для меню
    """
    navbar = [
        {'url': 'index', 'label': 'Главная'}
    ]

    if request.user.is_authenticated:
        navbar += [
            {'label': 'Авторизация', 'list': [{'url': 'logout', 'label': "Выйти"}]},
            {'label': 'Товары', 'list': [{'url': 'catalogue_list', 'label': "Каталог"},
                                         {'url': 'create_offer', 'label': "Создать"}]},
            {'label': 'Заказы', 'url':  'orders_list'}
        ]
    else:
        navbar += [
            {'label': 'Авторизация', 'list': [
                {'url': 'login', 'label': 'Войти'},
                {'url': 'register', 'label': 'Зарегистрироваться'}
            ]}
        ]
    return off_current(nav=navbar, req=request)
