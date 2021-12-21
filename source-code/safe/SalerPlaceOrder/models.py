from django.db import models

class Company(models.Model):
    DoesNotExist = None
    companyid = models.CharField(max_length=200)
    companyname = models.CharField(max_length=200)


class SalerInfo(models.Model):
    salerid = models.CharField(max_length=200)
    orderid = models.CharField(max_length=200)
    companyid = models.CharField(default=0, max_length=200)
