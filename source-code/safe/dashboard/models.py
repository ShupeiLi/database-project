from django.db import models
from register.models import NewUser


# Create your models here.
class OrderInformation(models.Model):
    ono = models.IntegerField(primary_key=True, unique=True, null=False)
    otime = models.DateField(null=False)
    ovalue = models.DecimalField(max_digit=8, decimal_places=2, null=False)
    username = models.ForeignKey(to=NewUser,related_name="username")  # Uno
    sellername = models.ForeignKey(to=NewUser,related_name="username")  # Sno
    otype = models.CharField(max_length=64, null=False)
    onum = models.IntegerField(max_length=4, null=False)

    def __str__(self):
        return self.ono

