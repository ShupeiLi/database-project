from django.db import models


class SalerInfo(models.Model):
    salerid = models.CharField(max_length=200)
    orderid = models.CharField(max_length=200)
    companyid = models.CharField(max_length=200)

class Company(models.Model):
    companyid = models.CharField(default=0, max_length=200)
    companyname = models.CharField(max_length=200)
