from django.urls import path

from main.modules import CatalogueView
from main.modules.product_card import ProductPageView
from main.views import OfferDetails, OfferEdit

urlpatterns = [
    path('', CatalogueView.as_view(), name='catalogue_list'),
    # path('<id>/', OfferDetails.as_view(), name='offer_by_sku'),
    path('<id>/', ProductPageView.as_view(), name='offer_by_sku'),
    path('<shopSku>/edit/', OfferEdit.as_view(), name='offer_by_sku_edit')
]
