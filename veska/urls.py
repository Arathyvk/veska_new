from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('allauth.urls')),
    path('',include('users.urls')),
    path('customers/',include('customers.urls')),
    path('newadmin/',include('admin_side.urls')),
    path('product_user/',include('product_user.urls')),
    path('cart_user/',include('cart_user.urls')),
    path('product_admin/',include('product_admin.urls')),
    path('category_admin/',include('category_admin.urls')),
    path('wishlist_user/',include('wishlist_user.urls')),
    path('order_user/',include('order_user.urls')),


]
