from django.db import models


# Create your models here.
class OrderInformation(models.Model):
    ono = models.IntegerField(primary_key=True, unique=True, null=False)
    otime = models.DateField(null=False)
    ovalue = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    username = models.ForeignKey('register.NewUser', related_name='usernames', on_delete=models.CASCADE)  # Uno
    sellername = models.ForeignKey('register.NewUser', related_name='sellernames', on_delete=models.CASCADE)  # Sno
    otype = models.CharField(max_length=64, null=False)
    onum = models.IntegerField(null=False)

    def __str__(self):
        return self.ono

