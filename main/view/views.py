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
    create_offer = serialize('create_offer')


class FormParser:
    def __init__(self, base_form):
        self.form_base = base_form
        self.form = None

    @staticmethod
    def check_model(model, attrs_for_filter):
        try:
            model = model.objects.filter(**attrs_for_filter)[0]
        except IndexError:
            return model.objects.create(**attrs_for_filter)
        return model

    def get_with_fill(self, model, attrs_for_filter, disabled) -> None:
        model = FormParser.check_model(model=model, attrs_for_filter=attrs_for_filter)
        self.form = self.form_base(instance=model)
        self.form.turn_off(disable=disabled)

    def get_without_fill(self, disabled) -> None:
        self.form = self.form_base()
        self.form.turn_off(disable=disabled)

    def post(self, request, model, attrs_for_filter, disabled) -> None:
        model = FormParser.check_model(model=model, attrs_for_filter=attrs_for_filter)
        self.form = self.form_base(request, instance=model)
        self.form.turn_off(disable=disabled)


class Multiform:
    def __init__(self):
        self.model_list = None
        self.models_json = {}

    def get_models_classes(self, key1: dict = None, key2: dict = None) -> None:
        # примеры смотрите в коде
        raise NotImplementedError

    def get_post_form(self, disable: bool, request) -> None:
        self.models_json.clear()
        for model in self.model_list:
            form = FormParser(base_form=model[2])
            form.post(request=request, model=model[0], attrs_for_filter=model[1], disabled=disable)
            self.models_json.update({str(model[2]()): form})

    def get_fill_form(self, disable) -> None:
        self.models_json.clear()
        for model in self.model_list:
            form = FormParser(base_form=model[2])
            form.get_with_fill(model=model[0], attrs_for_filter=model[1], disabled=disable)
            self.models_json.update(
                {str(model[2]()): form})

    def get_clear_form(self, disable) -> None:
        self.models_json.clear()
        for model in self.model_list:
            form = FormParser(base_form=model[2])
            form.get_without_fill(disabled=disable)
            self.models_json.update(
                {str(model[2]()): form})

    def get_form_for_context(self) -> dict:
        # примеры смотрите в коде
        raise NotImplementedError

    def is_valid(self) -> bool:
        for key, model in self.models_json.items():
            if not model.form.is_valid():
                return False
        return True

    def save(self) -> None:
        for key, model in self.models_json.items():
            model.form.save()
