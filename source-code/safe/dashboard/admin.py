from django.contrib import admin
from .models import OrderInformation, DeliveryInformation, RateSeller, RateDelivComp, HealthInformation, DistributionInformation, CompanyStaff, GeographicInformation, PandemicInformation

# Register your models here.
admin.site.register(OrderInformation)
admin.site.register(DeliveryInformation)
admin.site.register(RateSeller)
admin.site.register(RateDelivComp)
admin.site.register(HealthInformation)
admin.site.register(DistributionInformation)
admin.site.register(CompanyStaff)
admin.site.register(GeographicInformation)
admin.site.register(PandemicInformation)
