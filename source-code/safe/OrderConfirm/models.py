# -*- coding: utf-8 -*-

from django.db import models


class Order(models.Model):
    """
    Show orders to be confirmed and already confirmed
    """
    STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed')
    )
    Dno = models.CharField(max_length=100)
    Dvalue = models.FloatField(max_length=50)
    Dtrans = models.CharField(max_length=50)
    Tno = models.CharField(max_length=50)
    Sno = models.CharField(max_length=50)
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS)
    