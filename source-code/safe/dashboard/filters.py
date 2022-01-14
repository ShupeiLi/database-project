# -*- coding: utf-8 -*-

import django_filters
from .models import DeliveryInformation, RateSeller, RateDelivComp


# Information summary
class DeliveryFilter(django_filters.FilterSet):
    
    dvalue_min = django_filters.NumberFilter(field_name='dvalue', lookup_expr='gte')
    dvalue_max = django_filters.NumberFilter(field_name='dvalue', lookup_expr='lte')
    dtrans = django_filters.ChoiceFilter(field_name='dtrans', choices=(
        ('plane', '航空运输'), ('train', '铁道运输'), ('truck', '公路运输'),
        ))
    dsetime_min = django_filters.DateFilter(field_name="dsetime", lookup_expr='gte')
    dsetime_max = django_filters.DateFilter(field_name="dsetime", lookup_expr='lte')
    dretime_min = django_filters.DateFilter(field_name="dretime", lookup_expr='gte')
    dretime_max = django_filters.DateFilter(field_name="dretime", lookup_expr='lte')
    ovalue_min = django_filters.NumberFilter(field_name='order_information__ovalue', lookup_expr='gte')
    ovalue_max = django_filters.NumberFilter(field_name='order_information__ovalue', lookup_expr='lte')
    otype = django_filters.ChoiceFilter(field_name='order_information__otype', choices=(
        ("food", "food"), ("clothes", "clothes"), ("daily use", "daily use"), 
        ("digital", "digital"), ("office supplies", "office supplies"), ("sports","sports")
        ))
    onum_min = django_filters.NumberFilter(field_name='order_information__onum', lookup_expr='gte')
    onum_max = django_filters.NumberFilter(field_name='order_information__onum', lookup_expr='lte')    
    
    class Meta:
        model = DeliveryInformation
        fields = ['dno']
        
        
# Seller ratings
class SellerRatingFilter(django_filters.FilterSet):

    quality_min = django_filters.NumberFilter(field_name='quality', lookup_expr='gte')
    quality_max = django_filters.NumberFilter(field_name='quality', lookup_expr='lte')   
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')  
    look_min = django_filters.NumberFilter(field_name='look', lookup_expr='gte')
    look_max = django_filters.NumberFilter(field_name='look', lookup_expr='lte')
    delivery_min = django_filters.NumberFilter(field_name='delivery', lookup_expr='gte')
    delivery_max = django_filters.NumberFilter(field_name='delivery', lookup_expr='lte')    
    service_min = django_filters.NumberFilter(field_name='service', lookup_expr='gte')
    service_max = django_filters.NumberFilter(field_name='service', lookup_expr='lte')       

    class Meta:
        model = RateSeller
        fields = ['sellername_id']

        
# Company ratings
class CompanyRatingFilter(django_filters.FilterSet):

    speed_min = django_filters.NumberFilter(field_name='speed', lookup_expr='gte')
    speed_max = django_filters.NumberFilter(field_name='speed', lookup_expr='lte')   
    package_min = django_filters.NumberFilter(field_name='package', lookup_expr='gte')
    package_max = django_filters.NumberFilter(field_name='package', lookup_expr='lte')  
    perfection_min = django_filters.NumberFilter(field_name='perfection', lookup_expr='gte')
    perfection_max = django_filters.NumberFilter(field_name='perfection', lookup_expr='lte')  
    service_min = django_filters.NumberFilter(field_name='service', lookup_expr='gte')
    service_max = django_filters.NumberFilter(field_name='service', lookup_expr='lte')    
    timely_feedback_min = django_filters.NumberFilter(field_name='timely_feedback', lookup_expr='gte')
    timely_feedback_max = django_filters.NumberFilter(field_name='timely_feedback', lookup_expr='lte')         

    class Meta:
        model = RateDelivComp
        fields = ['compname_id']
