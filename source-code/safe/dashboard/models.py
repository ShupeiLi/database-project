from django.db import models

# Create your models here.

# User Profile
class Profile(models.Model):


    def __str__(self):
        return self.username
