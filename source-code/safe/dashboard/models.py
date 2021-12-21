from django.db import models


# Create your models here.
class RateSeller(models.Model):
    id = models.AutoField(primary_key=True)
    quality = models.IntegerField()
    price = models.IntegerField()
    look = models.IntegerField()
    delivery = models.IntegerField()
    service = models.IntegerField()

    def __str__(self):
        return self.id


class RateDelivComp(models.Model):
    id = models.CharField(primary_key=True,max_length=64)
    speed = models.IntegerField()
    package = models.IntegerField()
    perfection = models.IntegerField()
    service = models.IntegerField()
    timely_feedback = models.IntegerField()

    def __str__(self):
        return self.id


class OrderBuyer(models.Model):
    id = models.CharField(primary_key=True,max_length=64)
    type = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    number = models.IntegerField()
    order_date = models.DateField()

    def __str__(self):
        return self.id


class OrderSeller(models.Model):
    id = models.CharField(primary_key=True,max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    number = models.IntegerField()
    order_date = models.DateField()

    def __str__(self):
        return self.id


class OrderEbPlat(models.Model):
    id = models.CharField(primary_key=True,max_length=64)
    type = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    order_date = models.DateField()

    def __str__(self):
        return self.id


class OrderDelivComp(models.Model):
    id = models.CharField(primary_key=True,max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    order_date = models.DateField()
    in_time = models.CharField(max_length=64)

    def __str__(self):
        return self.id
