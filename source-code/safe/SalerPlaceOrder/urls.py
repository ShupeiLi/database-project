from django.urls import path

from . import views

urlpatterns = [
    path('', views.placeorder, name='placeorder'),
    path('<int:orderid>/result/', views.result, name='result'),
]