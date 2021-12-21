from django.db import models


# Create your models here.
class OrderInformation(models.Model):
    ono = models.IntegerField(primary_key=True, unique=True, null=False)
    otime = models.DateField(null=False)
    ovalue = models.FloatField(max_length=8, null=False)
    username = models.CharField(max_length=64, null=False)  # Uno
    sellername = models.CharField(max_length=64, null=False)  # Sno
    otype = models.CharField(max_length=64, null=False)
    onum = models.IntegerField(max_length=4, null=False)

    def __str__(self):
        return self.ono

