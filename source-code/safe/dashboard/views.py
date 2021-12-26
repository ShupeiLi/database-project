from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import OrderInformation, DeliveryInformation, HealthInformation, DistributionInformation
from django.urls import reverse_lazy
from django.contrib import messages
from .tools import encrypt


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


# Delivery: Submit today's health information (homepage)
@login_required
def delivery_health_homepage(request):
    username = request.COOKIES.get("username")
    health = HealthInformation.objects.filter(pno_id=username)
    context = {
        'health': health,
        'username': username,
    }
    return render(request, 'delivery-health-home.html', context)


# Delivery Historical Data
@login_required
def delivery_health_view(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")

    health = HealthInformation.objects.order_by('-pupdate')

    context={"username": username, "usertype": usertype, "health":health}

    return render(request, "delivery-health-view.html", context)


# Delivery Health Update
@login_required
def delivery_health_update(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")
    pno = get_object_or_404(User, username=username)
    
    if request.method == "POST":
        pcity = request.POST['pcity']
        ptemp = request.POST['ptemp']
        
        if not pcity:
            messages.warning(request, '必须输入今日经过城市')
            return redirect(reverse("dashboard:delivery-health-update"))
        if not ptemp:
            messages.warning(request, '必须输入今日体温')
            return redirect(reverse("dashboard:delivery-health-update"))

        health = HealthInformation.objects.create_healthinfo(pno=pno, pcity=pcity, ptemp=ptemp)
        health.save() 
        messages.success(request, '填写成功!')
        return redirect(reverse("dashboard:delivery-health-view"))

    context = {
        'username': pno,
        'usertype': usertype
    }
    return render(request, 'delivery-health-update.html', context)

         
# Delivery: Confirm the order distribution
@login_required          
def delivery_distribution_homepage(request):
    username = request.COOKIES.get("username")
    distribution = DistributionInformation.objects.filter(pno_id=username)
    distribution_count = distribution.count()
    distribution_p_count = DistributionInformation.objects.filter(pno_id=username).filter(is_checked=False).count()
    distribution_c_count = DistributionInformation.objects.filter(pno_id=username).filter(is_checked=True).count()

    if request.is_ajax and request.POST.get('distribution_confirm'):
        confirm_distribution_id = request.POST.get('distribution_confirm')
        confirm_distribution = distribution.objects.get(dpno = confirm_distribution_id) 
        confirm_distribution.is_checked = True
        distribution = confirm_distribution.save()
        return redirect(reverse("dashboard:delivery-distribution-home"))

    context = {
        'distribution_count': distribution_count,
        'distribution_p_count': distribution_p_count,
        'distribution_c_count': distribution_c_count,
        'distribution': distribution,
        'username': username,
    }     
    return render(request, 'delivery-distribution-home.html', context)
