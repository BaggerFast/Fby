from django.urls import path
from main.modules import *
# from main.view import OfferEdit

urlpatterns = [
    path('', CatalogueView.as_view(), name='catalogue_list'),
    path('create/', CreateOfferView.as_view(), name="create_offer"),
    path('<id>/', ProductPageView.as_view(), name='offer_by_sku'),
    # path('<id>/', OfferDetails.as_view(), name='offer_by_sku'),
    # path('<shopSku>/edit/', OfferEdit.as_view(), name='offer_by_sku_edit')
]
