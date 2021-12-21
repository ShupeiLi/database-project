from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^pie/$', views.ChartView.as_view(), name='demo'),
    url(r'^index/$', views.IndexView.as_view(), name='demo'),
]