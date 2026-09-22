from django.urls import path
from . import views

urlpatterns=[
    path('',                 views.admin_coupon_list,   name='admin_coupon_list'),
    path('add/',             views.admin_coupon_add,    name='admin_coupon_add'),
    path('<int:pk>/edit/',   views.admin_coupon_edit,   name='admin_coupon_edit'),
    path('<int:pk>/toggle/', views.admin_coupon_toggle, name='admin_coupon_toggle'),
    path('<int:pk>/delete/', views.admin_coupon_delete, name='admin_coupon_delete'),
]