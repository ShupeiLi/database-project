# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health, name='health'),
    path('createhealth/', views.create_health, name='createhealth'),
    path('distribution/', views.distribution, name='distribution'),
    path('confirmdistribution/<str:pk>/', views.confirm_distribution, name='confirmdistribution'),
    path('deletedistribution/<str:pk>/', views.delete_distribution, name='deletedistribution')
]


