from django.urls import path

from . import views

urlpatterns = [
    path('', views.placeorder, name='placeorder'),
    path('result/<int:orderid>/', views.result, name='result'),
]