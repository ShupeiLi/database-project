from django.contrib import admin
from .models import GeographicInformation, PandemicInformation

# Register your models here.
admin.site.register(GeographicInformation)
admin.site.register(PandemicInformation)
