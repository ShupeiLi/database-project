from django.db import models
from register.models import NewUser
from .tools import encrypt


class OrderInformation(models.Model):
    ono = models.CharField(primary_key=True, max_length=32, unique=True, null=False)
    otime = models.DateField(null=False)
    ovalue = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    username = models.ForeignKey('register.NewUser', related_name='usernames', on_delete=models.CASCADE)  # Uno
    sellername = models.ForeignKey('register.NewUser', related_name='sellernames', on_delete=models.CASCADE)  # Sno
    platformname = models.ForeignKey('register.NewUser', related_name='platformnames', on_delete=models.CASCADE) # 数据来源
    otype = models.CharField(max_length=64, null=False)
    onum = models.IntegerField(null=False)

    def __str__(self):
        return self.ono


class DeliveryInformationManager(models.Manager):

    def create_deliveryinfo_seller(self, ono, dtrans, tno, sno):

        # encrypt
        dno = encrypt(ono)

        if not ono:
            raise ValueError('必须提供有效订单号')
        if not dtrans:
            raise ValueError('必须选择运输方式')
        if not tno:
            raise ValueError('必须选择物流公司')
        
        deliveryinfo = self.model(
            dno=dno, dtrans=dtrans, tno=tno, sno=sno
            )

        deliveryinfo.save(using=self._db)
    
        return deliveryinfo
    
    def create_deliveryinfo_logistics(self, dno, dvalue, dsetime, dretime, is_checked):

        if not dvalue:
            raise ValueError('必须提供订单价格')
        if not dsetime:
            raise ValueError('必须填写发货时间')
        if not dretime:
            raise ValueError('必须填写预计到达时间')
        if not dretime:
            raise ValueError('必须选择是否接单')

        newinfo = {'dvalue':dvalue, 'dsetime':dsetime, 'dretime':dretime, 'is_checked':is_checked}
        DeliveryInformation.objects.filter(dno=dno).update(**newinfo)

        deliveryinfo = DeliveryInformation.objects.get(dno=dno)

        return deliveryinfo


class DeliveryInformation(models.Model):
    objects = DeliveryInformationManager()
    dno = models.CharField(primary_key=True, max_length=32, null=False, unique=True) # one to one
    dvalue = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    dtrans = models.CharField(max_length=128)
    tno = models.ForeignKey(NewUser, related_name='DeliveryInformation_NewUser_log', on_delete=models.CASCADE)    # one to one
    sno = models.ForeignKey(NewUser, related_name='DeliveryInformation_NewUser_seller', on_delete=models.CASCADE)    # one to one
    dsetime = models.DateField(max_length=128, null=True)
    dretime = models.DateField(max_length=128, null=True)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.dno