from django.urls import path
from main.modules.offers import CatalogueView, CreateOfferView, ProductPageView

urlpatterns = [
    path('', CatalogueView.as_view(), name='catalogue_offer'),
    path('create/', CreateOfferView.as_view(), name="create_offer"),
    path('<int:pk>/', ProductPageView.as_view(), name='offer_by_sku'),
]
