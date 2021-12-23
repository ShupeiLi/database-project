# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'dashboard'   

urlpatterns = [
    path('', views.board_home, name = "boardhome"),
    path('logistics-risk/', views.profile, name = "profile"),
    path('profile/', views.profile, name = "profile"),
    path('profile/update/', views.update_profile, name = "update_profile"),
    path('delivery-health/', views.delivery_health, name = "delivery_health"),
    path('submit-order/', views.seller_order_submitted, name="submitorder"),
]