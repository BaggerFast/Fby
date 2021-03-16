import json
from rest_framework import generics
from main.models.base import Offer
from main.serializers import OfferSerializer


class OfferList(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()


class OfferDetails(generics.RetrieveAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    lookup_field = 'shopSku'


class OfferEdit(generics.UpdateAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    lookup_field = 'shopSku'


def get_catalogue_from_file(file):
    """Загрузка каталога из файла file"""
    return json.load(open(file, "r", encoding="utf-8"))


def get_json_data_from_file(file):
    """
    Загрузка каталога из файла file
    """
    with open(file, "r", encoding="utf-8") as read_file:
        json_object = json.load(read_file)
    return json_object


def serialize(page):
    return 'pages/' + page + '.html'


class Page:
    index = serialize('index')
    registration = serialize('registration')
    login = serialize('login')
    catalogue = serialize('catalogue')
