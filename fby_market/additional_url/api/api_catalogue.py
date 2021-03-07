from django.urls import path
from main.views import catalogue_list, offer_by_sku, offer_by_sku_edit


urlpatterns = [
    path('', catalogue_list, name='catalogue_list'),
    path('<sku>/', offer_by_sku, name='offer_by_sku'),
    path('<sku>/edit/', offer_by_sku_edit, name='offer_by_sku_edit')
]
