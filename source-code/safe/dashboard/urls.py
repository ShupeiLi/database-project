# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'dashboard'   

urlpatterns = [
    path('', views.board_home, name = "board-home"),
    path('submit-order/', views.seller_order_submitted, name="submit-order"),
    path('confirm-order/', views.company_confirm_homepage, name="confirm-order-homepage"),
    path('confirm-order/update/<slug:dno>/', views.company_confirm_update_order, name='confirm-order-update'),
    path('health/', views.health, name='health'),
    path('createhealth/', views.create_health, name='createhealth'),
    path('distribution/', views.distribution, name='distribution'),
    path('confirmdistribution/<str:pk>/', views.confirm_distribution, name='confirmdistribution'),
]