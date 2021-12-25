from django.urls import path

from . import views

urlpatterns = [
    path('<int:orderid>/', views.getdata, name='Visualization'),
]