# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import SalerInfo, Company

def placeorder(request):
    try:
        selected_company = Company.companyname.get(pk=request.POST['company'])
    except (KeyError, Company.DoesNotExist):
        # 未提交公司选项，重新展示表单
        return render(request, 'SalerPlaceOrder/placeorder.html', {
            'error_message': "You didn't select a company.",
        })
    else:
        """
           将数据写入库
        """
        salerid = request.POST.get('salerid')  # 获取前端输入的卖方id
        orderid = request.POST.get('orderid')  # 获取前端输入的物流订单id
        company = request.POST.get('company')  # 获取前端选择的物流公司
        """
           跳转链接（卖家主页），不写死
           给出我们想要跳转的视图的名字和该视图所对应的URL模式中需要给该视图提供的参数
        """
        return HttpResponseRedirect(reverse('results', args=(salerid,)))

def result(request, orderid):
    salerid = get_object_or_404(SalerInfo, pk=orderid)
    return render(request, 'SalerPlaceorder/salerhome.html', {'salerid': salerid})
