# -*- coding: utf-8 -*-

import django_filters
from .models import DeliveryInformation


class DeliveryFilterCompany(django_filters.FilterSet):
    
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