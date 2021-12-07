# -*- coding: utf-8 -*-

from django.db import models


class Order(models.Model):
    """
    Show the information of the orders
    """
    STATUS = (
        ('pending', '待确认'),
        ('confirmed', '已确认')
    )
    Dno = models.CharField(max_length=100)
    Dvalue = models.DecimalField(max_digits=50, decimal_places=2)
    Tno = models.CharField(max_length=100)
    Sno = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS)
    