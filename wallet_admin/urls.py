from django.urls import path
from . import views

urlpatterns = [

    path('',                                views.admin_wallet_list,        name='admin_wallet_list'),
    path('<int:wallet_id>/',                views.admin_wallet_detail,      name='admin_wallet_detail'),
    path('<int:wallet_id>/adjust/',         views.admin_wallet_adjust,      name='admin_wallet_adjust'),
    path('<int:order_id>/approve-return/',  views.admin_approve_return,     name='admin_approve_return'),
    
]