# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'dashboard'   

urlpatterns = [
    path('', views.board_home, name = "board-home"),
    path('submit-order/', views.seller_order_submitted, name="submit-order"),
    path('confirm-order/', views.company_confirm_homepage, name="confirm-order-homepage"),
    path('confirm-order/update/<slug:dno>/', views.company_confirm_update_order, name='confirm-order-update'),
    path('delivery-health/', views.delivery_health_homepage, name='delivery-health-home'),
    path('delivery-health/update/<str:pk>/', views.delivery_health_update, name='delivery-health-update'),
    path('delivery-distribution/', views.delivery_distribution_homepage, name='delivery-distribution-home'),
    path('delivery-distribution/update/<str:pk>/', views.delivery_distribution_confirm, name='delivery-distribution-confirm'),
]