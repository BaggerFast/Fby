from rest_framework import generics

from main.models.ya_market.base import Offer
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
        {'url': 'index', 'label': 'Главная', 'list': False}
    ]

    if request.user.is_authenticated:
        navbar += [
            {'label': 'Авторизация', 'list': [{'url': 'logout', 'label': "Выйти"}]},
            {'label': 'Каталог', 'list': [{'url': 'catalogue_list', 'label': "Товары"}]}
        ]
    else:
        navbar += [
            {'label': 'Авторизация', 'list': [
                {'url': 'login', 'label': 'Войти'},
                {'url': 'register', 'label': 'Зарегистрироваться'}
            ]}
        ]

    # for menu_item in navbar:
    #     menu_item['active'] = request.path != reverse(menu_item['url'])

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
