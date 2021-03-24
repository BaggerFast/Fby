from django.urls import reverse
from rest_framework import generics
from main.models import *
from main.serializers import OfferSerializer


class OfferList(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()


class OfferDetails(generics.RetrieveAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    lookup_field = 'id'


class OfferEdit(generics.UpdateAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    lookup_field = 'shopSku'


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
            {'label': 'Товары', 'list': [{'url': 'catalogue_list', 'label': "Каталог"}]}
        ]
    else:
        navbar += [
            {'label': 'Авторизация', 'list': [
                {'url': 'login', 'label': 'Войти'},
                {'url': 'register', 'label': 'Зарегистрироваться'}
            ]}
        ]

    for menu_item in navbar:
        if menu_item.get('list', False):
            # для атрибута меню с выпадающим списком
            for i in range(len(menu_item['list'])):
                menu_item['list'][i]['active'] = request.path != reverse(menu_item['list'][i]['url'])
        else:
            # для обычных атрибутов
            menu_item['active'] = request.path != reverse(menu_item['url'])

    return navbar


def serialize(page) -> str:
    return f'pages/{page}.html'


class Page:
    """
    Для простого взаимодействия с путями файлов html
    """
    index = serialize('index')
    registration = serialize('registration')
    login = serialize('login')
    catalogue = serialize('catalogue')
    product_card = serialize('product_card')
