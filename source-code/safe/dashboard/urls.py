# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'dashboard'   

urlpatterns = [
    path('', views.board_home, name = "boardhome"),
    path('profile/', views.profile, name = "profile"),
    path('profile/update/', views.update_profile, name = "update_profile"),
]