from django.urls import path
from main.modules import *
# from main.view import OfferEdit

urlpatterns = [
    path('', CatalogueView.as_view(), name='catalogue_list'),
    # path('<id>/', OfferDetails.as_view(), name='offer_by_sku'),
    path('<id>/', ProductPageView.as_view(), name='offer_by_sku'),
    # path('<shopSku>/edit/', OfferEdit.as_view(), name='offer_by_sku_edit')
]
