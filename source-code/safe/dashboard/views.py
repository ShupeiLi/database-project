from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import OrderInformation, DeliveryInformation, RateSeller, RateDelivComp
from django.urls import reverse_lazy
from django.contrib import messages
from .tools import encrypt
from .filters import DeliveryFilterCompany, OrderFilterBuyer
from datetime import datetime


User = get_user_model()


# Homepage
@login_required
def board_home(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")
    return render(request, "board-home.html", 
                  context={"username": username, "usertype": usertype})


# Seller: Submit a new delivery order
@login_required
def seller_order_submitted(request):
    sno = request.COOKIES.get("username")
    companys = User.objects.filter(utype="company")
    if request.method == 'POST':
        ono = request.POST.get('ono')
        if OrderInformation.objects.filter(ono=ono).filter(sellername_id=sno).exists():
            dno = encrypt(ono)
            if not DeliveryInformation.objects.filter(dno=dno).exists():
                ono = OrderInformation.objects.get(ono=request.POST.get('ono')).ono
                tno = get_object_or_404(User, username=request.POST.get('tno'))
                sno_instance = get_object_or_404(User, username=sno)
                dtrans = request.POST.get('dtrans')
                new_delivery = DeliveryInformation.objects.create_deliveryinfo_seller(ono, dtrans, tno, sno_instance)
                new_delivery.save()
                messages.info(request, "提交成功")
                return HttpResponseRedirect(reverse_lazy("dashboard:submit-order"))
            else:
                messages.info(request, "订单已存在")
        else:
            messages.info(request, "请输入有效订单号")
    
    return render(request, "seller-order-submit.html", 
                  context={'companys':companys, "username": sno})


# Stat Page: calculate and send statistics data.
@login_required
def stat_func(request):
    gen_type = ["food", "clothes", "daily use", "digital", "office supplies", "sports"]
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")
    # year = request.POST.get("year")
    if usertype == "buyer":
        order = OrderInformation.objects.filter(username = username)
        order_type = [o.otype for o in order]
        type = [order_type.count(i) for i in gen_type]
        order_date = [o.otime.month for o in order]
        date = [order_date.count(i) for i in range(1,13)]
        return render(request, "stat_page.html",
                      {"username": username, "usertype": usertype, "type": type, "time": date})
    elif usertype == "seller":
        order = OrderInformation.objects.filter(sellername = username)
        rate = RateSeller.objects.get(sellername = username)
        rateNum = [float(rate.quality), float(rate.price), float(rate.look), float(rate.delivery), float(rate.service)]
        income = [0] * 12
        for o in order:
            income[o.otime.month - 1] += float(o.ovalue)
        return render(request, "stat_page.html", {"username": username, "usertype": usertype, "rate": rateNum, "income": income})
    elif usertype == "platform":
        order = OrderInformation.objects.filter(platformname = username)
        order_type = [o.otype for o in order]
        type = [order_type.count(i) for i in gen_type]
        volume = [0] * 12
        for o in order:
            volume[o.otime.month - 1] += float(o.ovalue)
        return render(request, "stat_page.html",
                      {"username": username, "usertype": usertype, "type": type, "volume": volume})
    elif usertype == "company":
        order = DeliveryInformation.objects.filter(tno = username)
        rate = RateDelivComp.objects.get(compname = username)
        rateNum = [float(rate.speed), float(rate.package), float(rate.perfection), float(rate.service), float(rate.timely_feedback)]
        income = [0] * 12
        for o in order:
            income[o.dsetime.month - 1] += float(o.dvalue)
        return render(request, "stat_page.html", {"username": username, "usertype": usertype, "rate": rateNum, "income": income})
    else:
        messages.info("错误用户类型！")

    return render(request, "stat_page.html")


# Company: Confirm a delivery order (homepage)
@login_required
def company_confirm_homepage(request):
    """
    Show the number of different orders and the details.
    """
    username = request.COOKIES.get("username")
    order = DeliveryInformation.objects.filter(tno_id=username)
    order_count = order.count()

    order_p_count = DeliveryInformation.objects.filter(tno_id=username).filter(is_checked=False).count()
    order_c_count = DeliveryInformation.objects.filter(tno_id=username).filter(is_checked=True).count()

    if request.is_ajax and request.POST.get('order_del'):
        del_order_id = request.POST.get('order_del')
        del_order = DeliveryInformation.objects.get(dno = del_order_id)
        del_order.delete()

    context = {
        'order_count': order_count,
        'order_p_count': order_p_count,
        'order_c_count': order_c_count,
        'order': order,
        'username': username,
    }
    
    return render(request, 'company-confirm-home.html', context)    
            
        
# Company: Confirm a delivery order (update)
@login_required
def company_confirm_update_order(request, dno):
    """
    Post whether to change the status of the order (is_checked).
    """
    username = request.COOKIES.get("username")
    order = DeliveryInformation.objects.get(dno=dno)

    if request.method == 'POST':
        dvalue = request.POST.get('dvalue')
        dsetime = request.POST.get('dsetime')
        dretime = request.POST.get('dretime')
        is_checked = True
        order = DeliveryInformation.objects.filter(dno=dno)
        DeliveryInformation.objects.create_deliveryinfo_logistics(dno, dvalue, dsetime, dretime, is_checked)
        return redirect(reverse_lazy("dashboard:confirm-order-homepage"))

    context = {
        'order': order,
        'username': username,
    }
    return render(request, 'company-confirm-update-order.html', context)


# Buyer-information-summary: Search orders
@login_required
def buyer_information_summary_orders(request):
    """
    Search information from orderinformation and deliveryinformation tables.
    """
    username = request.COOKIES.get("username")
    product_orders = OrderInformation.objects.filter(username_id=username)
    product_filter = OrderFilterBuyer(request.GET, queryset=product_orders)
    product_orders = product_filter.qs
    
    context = {
        'username': username,
        'product_filter': product_filter,
        'product_orders': product_orders,
    }
    return render(request, 'information-summary-buyer.html', context)


# Company-information-summary: Search orders
@login_required
def company_information_summary_orders(request):
    """
    Search information from orderinformation and deliveryinformation tables.
    """
    username = request.COOKIES.get("username")
    delivery_orders = DeliveryInformation.objects.filter(tno_id=username)
    delivery_filter = DeliveryFilterCompany(request.GET, queryset=delivery_orders)
    delivery_orders = delivery_filter.qs
    
    context = {
        'username': username,
        'delivery_filter': delivery_filter,
        'delivery_orders': delivery_orders,
    }
    return render(request, 'information-summary-company.html', context)