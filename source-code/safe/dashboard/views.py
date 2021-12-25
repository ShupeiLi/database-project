from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import OrderInformation, DeliveryInformation, RateSeller, RateDelivComp
from django.urls import reverse_lazy
from django.contrib import messages
from .tools import encrypt
from datetime import datetime


User = get_user_model()

# Create your views here.
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
        if OrderInformation.objects.filter(ono=int(ono)).filter(sellername_id=sno).exists():
            dno = encrypt(ono)
            if not DeliveryInformation.objects.filter(dno=dno).exists():
                ono = OrderInformation.objects.get(ono=request.POST.get('ono')).ono
                tno = get_object_or_404(User, username=request.POST.get('tno'))
                sno_instance = get_object_or_404(User, username=sno)
                dtrans = request.POST.get('dtrans')
                new_delivery = DeliveryInformation.objects.create_deliveryinfo_seller(ono, dtrans, tno, sno_instance)
                new_delivery.save()
                messages.info(request, "提交成功")
                return HttpResponseRedirect(reverse_lazy("dashboard:submitorder"))
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
            
            
            