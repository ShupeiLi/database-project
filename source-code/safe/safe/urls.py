# -*- coding: utf-8 -*-

from django.contrib import admin
<<<<<<< HEAD
from django.urls import include, path
=======
from django.urls import path, include
>>>>>>> master

urlpatterns = [
    path('safelogistics/dashboard/', include('dashboard.urls')),
    path('safelogistics/', include('register.urls')),
    path('admin/', admin.site.urls),
    path('', include('OrderConfirm.urls')),
    path('', include('deliveryman.urls'))
]
