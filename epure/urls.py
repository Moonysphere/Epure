"""
URL configuration for epure project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from store.views import index, product_detail, add_to_cart, cart, delete_cart, page_user, valid_cart
from accounts.views import signup, logout_user, login_user

from django.conf.urls.static import static

from epure import settings

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('page_user/', page_user, name='page_user'),
    path('cart/', cart, name='cart'),
    path('cart/delete', delete_cart, name='delete_cart'),
    path('valid-cart/', valid_cart, name='valid_cart'),
    path('admin/', admin.site.urls),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/add_to_cart', add_to_cart, name="add_to_cart")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
