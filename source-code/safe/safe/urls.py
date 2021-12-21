# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('placeorder/', include(('SalerPlaceOrder.urls', "SalerPlaceOrder"), namespace='SalerPlaceOrder')),
    path('pathvisualization/', include(('PathVisualization.urls', "PathVisualization"), namespace='PathVisualization')),
    path('admin/', admin.site.urls),
]
