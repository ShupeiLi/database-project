# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('orderconfirm/', views.homepage, name='orderconfirm'),
    path('updateorder/<str:pk>/', views.update_order, name='updateorder'),
    path('deleteorder/<str:pk>/', views.delete_order, name='deleteorder')
]
