# -*- coding: utf-8 -*-

from django.urls import path, re_path
from . import views
from django.views.generic import TemplateView

app_name = "homepage"

urlpatterns = [
    path("", views.home, name = "home"),
    re_path(r'^login/', TemplateView.as_view(template_name = 'homepage/login.html'), name = 'login'),
]