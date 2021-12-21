from django.db import models


class SalerInfo(models.Model):
    salerid = models.CharField(max_length=200)
    orderid = models.CharField(max_length=200)
    company = models.CharField(max_length=200,default=0)
