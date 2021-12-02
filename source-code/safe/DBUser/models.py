from django.db import models


# 定义用户类
class DBUser(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    userType = models.CharField(max_length=32)
