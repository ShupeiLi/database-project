# -*- coding: utf-8 -*-

from django.shortcuts import render
from SalerPlaceOrder.models import Saler

def placeorder(request):
    request.encoding = 'utf-8'
    """
    在卖方订单表增加数据
    """
    result = ""
    # 用于返回是否输入成功
    if request.method == 'POST' and request.POST:
        #判断提交方式是否为POST及POST是否有值
        salerid = request.POST.get('salerid')
        #获取前端输入的卖方id
        orderid = request.POST.get('orderid')
        # 获取前端输入的物流订单id
        company = request.POST.get('company')
        # 获取前端选择的物流公司
        models.SaleInfo.objects.create(salerid=salerid, orderid=orderid, company=company)
        """
        SalerPlaceOrder.salerid = salerid
        SalerPlaceOrder.orderid = orderid
        SalerPlaceOrder.company = company
        SalerPlaceOrder.save()
        """
        result = 'success'
    return render(request, "salerhome.html", {'result':result})