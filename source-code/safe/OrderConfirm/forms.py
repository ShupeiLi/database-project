# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['time_created']
        labels = {
            'Dno': '物流单号',
            'Dvalue': '物流订单金额',
            'Tno': '物流公司编号',
            'Sno': '卖家编号',
            'status': '订单状态'
        }
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
            })
        }