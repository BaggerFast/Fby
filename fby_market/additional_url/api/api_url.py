from django.urls import path, include
import fby_market.additional_url.api.api_catalogue as catalogue
import fby_market.additional_url.api.api_account as accounts

urlpatterns = [
    path('catalogue/', include(catalogue)),
    path('accounts/', include(accounts))
]

