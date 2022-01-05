from django.db import models


# Create your models here.
class GeographicInformation(models.Model):
    dno = models.CharField(max_length=200)
    dloc = models.CharField(max_length=200)
    dupdate = models.DateTimeField(max_length=200)

    def __str__(self):
        return self.dno
    

class PandemicInformation(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    date = models.DateTimeField(max_length=6)
    place = models.CharField(max_length=200)
    number = models.CharField(max_length=200)

    def __str__(self):
        return self.id
