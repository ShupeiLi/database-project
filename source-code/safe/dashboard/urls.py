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
    path('information-summary-buyer/', views.buyer_information_summary_orders, name='information-summary-buyer'),
    path('information-summary-seller/', views.seller_information_summary_orders, name='information-summary-seller'),
    path('information-summary-platform/', views.platform_information_summary_orders, name='information-summary-platform'),
    path('information-summary-company/', views.company_information_summary_orders, name='information-summary-company'),
    path('search-scores-buyer/', views.buyer_view_seller_scores, name='search-scores-buyer'),
    path('search-scores-platform/', views.platform_view_seller_scores, name='search-scores-platform'),
    path('search-scores-seller/', views.seller_view_company_scores, name='search-scores-seller'),
    path('profile/', views.profile, name = "profile"),
    path('profile/update/', views.update_profile, name = "update_profile"),
    path('delivery-health-view/', views.delivery_health_view, name = "delivery-health-view"),
    path('delivery-health-update/', views.delivery_health_update, name = "delivery-health-update"),
    path('delivery-distribution/', views.delivery_distribution_homepage, name='delivery-distribution-home'),
    path('manage-staffs', views.company_manage_staffs, name="manage-staffs"),
    path('manage-staffs/history/<slug:pno>/', views.company_staff_history, name='manage-staffs-history'),
]