# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('placeorder/', include(('SalerPlaceOrder.urls', "SalerPlaceOrder"), namespace='SalerPlaceOrder')),
    path('safelogistics/dashboard/', include('dashboard.urls')),
    path('safelogistics/', include('register.urls')),
    path('admin/', admin.site.urls),
]
