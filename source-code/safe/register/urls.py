from django.urls import path
from . import views

app_name = 'register'   

urlpatterns = [
    path('', views.home, name = "home"),
    path('sign-up/', views.register, name='signup'),
    path('log-in/', views.login, name = 'login'),
]