# -*- coding: utf-8 -*-

from django.urls import path, re_path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.home, name = "safelogistics"),
    re_path(r'^login/', TemplateView.as_view(template_name = 'homepage/login.html'), name = 'login'),
    re_path(r'^sign/', TemplateView.as_view(template_name = 'homepage/sign.html'), name = 'sign'),
]