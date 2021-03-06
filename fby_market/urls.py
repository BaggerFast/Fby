"""fby_market URL Configuration

The `urlpatterns` list routes URLs to view. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function view
    1. Add an import:  from my_app import view
    2. Add a URL to urlpatterns:  path('', view.home, name='home')
Class-based view
    1. Add an import:  from other_app.view import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from fby_market import settings
from main.modules import MainView, FaqView
from fby_market.additional_url import Url

urlpatterns = [
    # basic
    path('', MainView.as_view(), name="index"),
    path('faq/', FaqView.as_view(), name="faq"),
    path('admin/', admin.site.urls),
    # nested
    path('catalogue/', include(Url.catalogue)),
    path('orders/', include(Url.orders)),
    path('profile/', include(Url.profile)),
    path('analytics/', include(Url.analytics)),
    # auth
    path('auth/', include(Url.auth)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
