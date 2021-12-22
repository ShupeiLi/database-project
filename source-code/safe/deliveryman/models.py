# -*- coding: utf-8 -*-

from django.db import models


class Health(models.Model):
    """
    Show the health information of the deliveryman
    """
    username = models.CharField(max_length=100)
    pcity = models.CharField(max_length=100)
    ptemp = models.DecimalField(max_digits=50, decimal_places=1)
    pupdate = models.DateTimeField(auto_now_add=True)
    
    
class Distribution(models.Model):
    """
    Show the order information distributed to a certain deliveryman
    """
    STATUS = (
        ('pending', '待确认'),
        ('confirmed', '已确认')
    )
    dpno = models.CharField(max_length=100)
    dno = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=STATUS)
    

    