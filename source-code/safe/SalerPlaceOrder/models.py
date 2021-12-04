from django.db import models


class Saler(models.Model):
    salerid = models.CharField(max_length=20)
    orderid = models.CharField(max_length=20)
    company = models.CharField(max_length=20)