# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import SalerInfo, Company


def placeorder(request):
    try:
        selected_company = Company.objects.get(pk=request.POST['company'])  # 获取前端选择的物流公司
    except (KeyError, Company.DoesNotExist):
        # 未给出公司选项，重新展示表单
        return render(request, 'SalerPlaceOrder/placeorder.html', {
            'error_message': "You didn't select a company.",
        })
    else:
        if request.method == 'POST':
            selected_company = Company.objects.get(pk=request.POST['company'])  # 获取前端选择的物流公司
            input_salerid = request.POST.get('salerid')  # 获取前端输入的卖方id
            input_orderid = request.POST.get('orderid')  # 获取前端输入的物流订单id
            SalerInfo.objects.create(
                orderid = input_orderid,
                salerid = input_salerid,
                company = selected_company
        )
    """
   跳转结果页
    """
    return HttpResponseRedirect(reverse('SalerPlaceOrder:result', args=(SalerInfo.orderid,)))

def result(request, orderid):
    orderid = get_object_or_404(SalerInfo, pk=orderid)
    return render(request, 'SalerPlaceorder/result.html', {'orderid': orderid})

def home(request, salerid):
    return HttpResponse("You're looking at homepage of saler %s." % salerid)
