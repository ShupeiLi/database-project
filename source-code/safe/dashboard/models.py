from django.db import models
from register.models import NewUser
from django.contrib.auth import get_user_model
from .tools import encrypt

User = get_user_model()


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
        
        order_information = OrderInformation.objects.get(ono=ono)
        buyer = order_information.username_id
        
        if not ono:
            raise ValueError('必须提供有效订单号')
        if not dtrans:
            raise ValueError('必须选择运输方式')
        if not tno:
            raise ValueError('必须选择物流公司')
        
        deliveryinfo = self.model(
            dno=dno, dtrans=dtrans, tno=tno, sno=sno, order_information=order_information, buyer=buyer
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
    order_information = models.OneToOneField(OrderInformation, null=True, related_name='doinfo', on_delete=models.CASCADE)
    dno = models.CharField(primary_key=True, max_length=32, null=False, unique=True) # one to one
    dvalue = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    dtrans = models.CharField(max_length=128)
    tno = models.ForeignKey(NewUser, related_name='DeliveryInformation_NewUser_log', on_delete=models.CASCADE)    # one to one
    sno = models.ForeignKey(NewUser, related_name='DeliveryInformation_NewUser_seller', on_delete=models.CASCADE)    # one to one
    dsetime = models.DateField(max_length=128, null=True)
    dretime = models.DateField(max_length=128, null=True)
    is_checked = models.BooleanField(default=False)
    buyer = models.ForeignKey(NewUser, related_name='DeliveryInformation_NewUser_buyer', on_delete=models.CASCADE)    # one to one

    objects = DeliveryInformationManager()

    def __str__(self):
        return self.dno


class RateSeller(models.Model):
    sellername = models.OneToOneField('register.NewUser', related_name='rateforseller', on_delete=models.CASCADE)
    quality = models.DecimalField(max_digits=2, decimal_places=1, null=True)  # 产品质量
    price = models.DecimalField(max_digits=2, decimal_places=1, null=True)  # 产品价格或性价比
    look = models.DecimalField(max_digits=2, decimal_places=1, null=True)  # 产品外观
    delivery = models.DecimalField(max_digits=2, decimal_places=1, null=True)  # 产品配送
    service = models.DecimalField(max_digits=2, decimal_places=1, null=True)  # 卖方客服服务情况

    def __str__(self):
        return self.sellername


class RateDelivComp(models.Model):
    compname = models.OneToOneField('register.NewUser', related_name='rateforcompany', on_delete=models.CASCADE)
    speed = models.DecimalField(max_digits=2, decimal_places=1, null=True)  # 配送速度
    package = models.DecimalField(max_digits=2, decimal_places=1, null=True)  # 包装质量
    perfection = models.DecimalField(max_digits=2, decimal_places=1, null=True)  # 配送后包裹完好度
    service = models.DecimalField(max_digits=2, decimal_places=1, null=True)  # 服务情况
    timely_feedback = models.DecimalField(max_digits=2, decimal_places=1, null=True)  # 及时提供数据（地理位置或健康信息），及时反馈

    def __str__(self):
        return self.compname


class HealthInformationManager(models.Manager):
    def create_healthinfo(self, pno, pcity, ptemp):

        if not pcity:
            raise ValueError('必须输入途径城市')
        if not ptemp:
            raise ValueError('必须输入今日体温')
        
        healthinfo = self.model(
            pno=pno, pcity=pcity, ptemp=ptemp
            )

        healthinfo.save(using=self._db)

        return healthinfo


class HealthInformation(models.Model):
    """
    Show the health information of all deliverymen
    """
    pno = models.ForeignKey(NewUser, related_name='HealthInformation_Deliverymanname', on_delete=models.CASCADE)    # one to one
    pcity = models.CharField(max_length=100)
    ptemp = models.DecimalField(max_digits=25, decimal_places=1)
    pupdate = models.DateField(auto_now_add=True)
    
    objects = HealthInformationManager()

    class Meta:
        verbose_name = '员工健康信息表'
        verbose_name_plural = verbose_name
        unique_together = ("pno", "pupdate")

    def __str__(self):
        return self.pcity

    
class DistributionInformation(models.Model):
    """
    Show the distribution of order to all deliveryman
    """
    pno = models.ForeignKey(NewUser, related_name='DistributionInformation_Deliverymanname', on_delete=models.CASCADE)    # one to one
    dpno = models.CharField(max_length=100,primary_key=True)
    dno = models.ForeignKey(DeliveryInformation, related_name='DistributionInformation_OrderNo', on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)
   
    def __str__(self):
        return self.dpno


class CompanyStaff(models.Model):
    """
    Show the relationship between the staff and the company
    """
    pno = models.ForeignKey(NewUser, related_name='CompanyStaff_Staffname', on_delete=models.CASCADE)    # one to one
    tno = models.ForeignKey(NewUser, related_name='CompanyStaff_Companyname', on_delete=models.CASCADE)    # one to one
   
    def __str__(self):
        return self.pno.username
   
    
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
        return str(self.id)
    

class GeographicTransformation(models.Model):
    dloc = models.CharField(max_length=200, primary_key=True, unique=True, null=False)
    dpro = models.CharField(max_length=200, null=True)
    dlat = models.DecimalField(max_digits=25, decimal_places=4)
    dlng = models.DecimalField(max_digits=25, decimal_places=4)
    
    def __str__(self):
        return self.dloc