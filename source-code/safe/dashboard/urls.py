# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'dashboard'   

urlpatterns = [
    path('', views.board_home, name = "boardhome"),
    path('submit-order/', views.seller_order_submitted, name="submitorder"),
    path('stat-page/', views.stat_func, name="stat_page"),
]