# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import SalerInfo


def placeorder(request):
    ctx={}
    if request.method == 'POST':
        selected_company = request.POST.get('company')  # 获取前端选择的物流公司
        input_salerid = request.POST.get('salerid')  # 获取前端输入的卖方id
        input_orderid = request.POST.get('orderid')  # 获取前端输入的物流订单id
        SalerInfo.objects.create(
            orderid=input_orderid,
            salerid=input_salerid,
            company=selected_company
        )
        ctx['rlt'] = 'success'
        return HttpResponseRedirect(reverse('SalerPlaceOrder:result', args=(input_orderid,)))
    else:
        ctx['rlt'] = 'error'
        return render(request, "SalerPlaceOrder/placeorder.html", ctx)

def result(request, orderid):
    orderid = get_object_or_404(SalerInfo, pk=orderid)
    '''
    主页不写在该AP本下，先用runoob链接代替了，此处需要替换为买家主页
    '''
    views_str = "<a href='https://www.runoob.com/'>点击跳转卖家主页</a>"
    return render(request, 'SalerPlaceorder/result.html', {"views_str": views_str})
