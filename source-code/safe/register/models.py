# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
 

class MyAccountManager(BaseUserManager):

    def create_user(self, username, password, utype, companyname, registerid, address, tel, email):

        if not username:
            raise ValueError('You must provide a username')
        if not password:
            raise ValueError('You must provide a valid password')
        if not utype:
            return ValueError('You must provide a user type')
        if not companyname:
            return ValueError('You must provide a companyname')
        if not registerid:
            return ValueError('You must provide a registerid')
        if not email:
            return ValueError('You must provide an email')

        user = self.model(
            username=username, utype=utype, companyname=companyname, registerid=registerid, 
            address=address, tel=tel, email=self.normalize_email(email)
            )

        user.set_password(password)
        user.save(using=self._db)
    
        return user
    
    def create_superuser(self, username, password, email, utype="admin", companyname="admin", 
                         registerid="admin", address="admin", tel="admin"):
        # create superuser here
        user = self.create_user(
            username, password, utype, companyname, registerid, address, tel, email
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class NewUser(AbstractBaseUser):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=255)
    utype = models.CharField(max_length=128)
    companyname = models.CharField(max_length=255)
    registerid = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    tel = models.CharField(max_length=11)
    email = models.EmailField(max_length=25)
    registerdate = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'utype', 'registerid', 'email']
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.username