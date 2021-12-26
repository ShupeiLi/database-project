# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from .models import HealthInformation, DistributionInformation

    
class HealthForm(ModelForm):
    """
    Show the health information of the deliveryman
    """
    class Meta:
        model = HealthInformation
        fields = '__all__'
        exclude = ['Pupdate']
        labels = {
            'pno': '配送人员',
            'pcity': '当日途经城市',
            'ptemp': '配送人员体温'
        }
        widgets = {
            'pcity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入当日途经城市'
            }),
            'ptemp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入当日体温'
            })
        }


class DistributionForm(ModelForm):
    """
    Show the order information distributed to a certain deliveryman
    """
    class Meta:
        model = DistributionInformation
        fields = '__all__'
        labels = {
            'dpno': '订单分配编号',
            'dno': '物流单号',
            'pno': '配送人员',
            'is_checked': '订单状态'
        }
        widgets = {
            'is_checked': forms.Select(attrs={
                'class': 'form-control',
            })
        }