from django.urls import path, include
import fby_market.additional_url.api.api_catalogue as catalogue

urlpatterns = [
    path('catalogue/', include(catalogue)),
    path('accounts/', include('rest_framework.urls')),
]
