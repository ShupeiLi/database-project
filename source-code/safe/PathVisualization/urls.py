from django.urls import path

from . import views

urlpatterns = [
    path('path/<int:orderid>/', views.showpath, name='showpath'),
]