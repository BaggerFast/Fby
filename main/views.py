from rest_framework import generics
from main.models.base import Offer
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


def serialize(page):
    return f'pages/{page}.html'


class Page:
    index = serialize('index')
    registration = serialize('registration')
    login = serialize('login')
    catalogue = serialize('catalogue')
