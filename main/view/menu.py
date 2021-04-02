from django.urls import reverse


def off_current(navbar: list, request):
    for menu_item in navbar:
        if menu_item.get('list', False):
            # для атрибута меню с выпадающим списком
            for i in range(len(menu_item['list'])):
                menu_item['list'][i]['active'] = request.path != reverse(menu_item['list'][i]['url'])
        else:
            # для обычных атрибутов
            menu_item['active'] = request.path != reverse(menu_item['url'])
    return navbar


def get_navbar(request) -> list:
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
                                         {'url': 'create_offer', 'label': "Создать"}]}
        ]
    else:
        navbar += [
            {'label': 'Авторизация', 'list': [
                {'url': 'login', 'label': 'Войти'},
                {'url': 'register', 'label': 'Зарегистрироваться'}
            ]}
        ]
    return off_current(navbar=navbar, request=request)
