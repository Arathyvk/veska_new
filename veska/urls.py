from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('django-admin/',       admin.site.urls),
    path('accounts/',           include('allauth.urls')),
    path('',                    include('users.urls')),
    path('customers/',          include('customers.urls')),
    path('newadmin/',           include('admin_side.urls')),
    path('product',             include('product_user.urls')),
    path('cart/',               include('cart_user.urls')),
    path('product/',            include('product_admin.urls')),
    path('category/',           include('category_admin.urls')),
    path('wishlist/',           include('wishlist_user.urls')),
    path('order/',              include('order_user.urls')),
    path('checkout_page/',      include('checkout_page.urls')),
    path('order_admin/',        include('order_admin.urls')),
    path('wallet/',             include('wallet_user.urls')),
    path('offer/',              include('offer_admin.urls')),
    path('coupon/',             include('coupon_admin.urls')),
    path('about/',              include('about_us.urls')),
    path('wallet/',             include('wallet_admin.urls')),
    path('dashboard/',          include('dashboard.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
handler403 = 'core.views.custom_403'
handler400 = 'core.views.custom_400'