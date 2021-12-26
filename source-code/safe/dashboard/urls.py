# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'dashboard'   

urlpatterns = [
    path('', views.board_home, name = "board-home"),
    path('submit-order/', views.seller_order_submitted, name="submit-order"),
    path('stat-page/', views.stat_func, name="stat_page"),
    path('confirm-order/', views.company_confirm_homepage, name="confirm-order-homepage"),
    path('confirm-order/update/<slug:dno>/', views.company_confirm_update_order, name='confirm-order-update'),
]