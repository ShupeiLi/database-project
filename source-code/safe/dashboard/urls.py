# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'dashboard'   

urlpatterns = [
    path('', views.board_home, name = "boardhome"),
    path('submit-order/', views.seller_order_submitted, name="submitorder"),
    path('health/', views.health, name='health'),
    path('createhealth/', views.create_health, name='createhealth'),
    path('distribution/', views.distribution, name='distribution'),
    path('confirmdistribution/<str:pk>/', views.confirm_distribution, name='confirmdistribution'),
]