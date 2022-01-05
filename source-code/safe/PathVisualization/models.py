from django.db import models


# Create your models here.
class GeographicInformation(models.Model):
    dno = models.CharField(max_length=200)
    dloc = models.CharField(max_length=200)
    dupdate = models.DateTimeField(max_length=200)
    

class PandemicInformation(models.Model):
    date = models.DateTimeField(max_length=6)
    place = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
