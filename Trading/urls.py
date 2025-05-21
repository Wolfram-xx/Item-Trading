"""
URL configuration for Trading project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.admin import site
from django.urls import path
from ads.views import *

urlpatterns = [
    path('admin/', site.urls),
    path('', index_page),
    path('home/', index_page),
    path('login/', login_me),
    path('reg/', reg),
    path("error_auth/", error_auth),
    path("profile/", profile_page),
    path("new_item/", new_item_page),
    path("new_item/create/", create_item),
    path("ad/", ad_page),
    path("ad/edit/", ad_edit),
    path("logout/", logout_me),
    path("market/", market_page),
    path("market/new_trade/", new_trade_page),
    path("market/create_trade/", create_trade),
    path("my_trades/", my_trades_page),
    path('new_trades/', trades_for_me_page),
    path('accept_trade/', accept_trade),
    path('deny_trade/', deny_trade),
    path('ad/delete/', delete_ad),
]
