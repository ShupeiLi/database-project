# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect, reverse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import OrderInformation, DeliveryInformation, RateSeller, RateDelivComp, HealthInformation
from django.urls import reverse_lazy
from django.contrib import messages
from .tools import encrypt
from .filters import DeliveryFilterCompany, OrderFilterBuyer

User = get_user_model()

# Homepage
@login_required
def board_home(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")
    return render(request, "board-home.html", 
                  context={"username": username, "usertype": usertype})


# Delivery Historical Data
@login_required
def delivery_health_view(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")

    health = HealthInformation.objects.order_by('-pupdate')

    context={"username": username, "usertype": usertype}

    return render(request, "delivery-health-view.html", context)


# Delivery Health Update
@login_required
def delivery_health_update(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")
    
    context={"username": username, "usertype": usertype}

    return render(request, "delivery-health-update.html", context) 


# Logistics Risk
@login_required
def logistics_risk(request):

    # overall risk score
    '''
    Description for overall risk score: 
    **district_tisk_score:
    1. for each delivery order we calculate the overall risk score (score is calculated by delivery order)
    2. for a specific delivery order, we may have several places and a specific dsetime and a dretime
    3. dloc_list -> the list of places on the delivery path, dloc_list = [(place1, starttime1, endtime1), ...], using zip can get this form
    4. starttime, endtime: the range of time which the delivery order stay in a specific place
    5. a delivery order can be conducted by severl staff (distinguished by 1), staff_list contains the staffs delivered this order, staff_list = [pno1, pno2, ...]
    6. we put more weight on staff than district risk, 0.8/0.2
    '''
    district_risk_score = 0
    for place, starttime, endtime in dloc_list:
        district_risk_score += district_risk_score(place, starttime, endtime, covid19)

    staff_risk_score = 0
    for pno in staff_list:
        staff_risk_score += staff_risk_score(pno, startime, arrivetime, health, covid19)

    # !!!!!!!!!!!!!!!!!!!! final overall risk score !!!!!!!!!!!!!!!!!!!!! #
    risk_socre = 0.2 * district_risk_score + 0.8 * staff_risk_score

    ############################################################################

    # delivery district risk score  
    '''
    delivery district risk score (range: .00-100.00) criteria (begin with .00):
    1. only care about case increaing in 14 days
    2. increase number in [0, 10]: += number * .1
    3. increase number in [11, 30]: += number * .2
    4. increase number in [31, 60]: += number * .5
    5. increase number > 60: += number * 1
    6. no new case in each 14 days (to now): * .2
    '''
    def district_risk_score(place, starttime, endtime, covid19):
        district_score = 0

        start_date = covid19['date'] >= starttime - datetime.timedelta(days=14)
        end_date = covid19['date'] <= endtime
        data = covid19[start_date & end_date] # this will be a pandas data frame contains col=['date', 'place', 'number']
        city_data = data[data['place'] == place] # specific place in specific date range

        district_score = city_data['number'].apply(cal_district_score).sum()

        return district_score

    # delivery staff risk score
    '''
    delivery staff risk score (range: .00-100.00) criteria (begin with .00):
    1. body temperature in [36.3, 37.2]: -
    2. body temperature < 36.3: += diff * 100
    3. body temperature > 37.2: += diff * 150
    4. path district risk score in 14 days: += (district risk at that time) * (temp_diff + .1)
    '''
    def staff_risk_score(pno, startime, arrivetime, health, covid19):
        staff_score = 0

        staff_health = health[health['pno'] == pno]
        start_date = staff_health['pupdate'] >= startime - datetime.timedelta(days=14)
        end_date = staff_health['pupdate'] <= arrivetime
        staff_health = staff_health[start_date & end_date] # now we get a specific staff's healthy info in his delivery date range

        pass_by_city = staff_health['pcity'].unique()
        passbycity_risk_score = 0
        for city in pass_by_city:
            passbycity_risk_score += district_risk_score(city, startime, arrivetime, covid19)

        health_risk_score = staff_health['temp'].apply(cal_staff_score).sum()

        staff_score = 0.2 * passbycity_risk_score + 0.8 * health_risk_score

        return staff_score

    # criteria: district
    def cal_district_score(number, score=0):
            if number >= 0  and number <= 10:
                score += number * 0.1
            elif number >= 11 and number <= 30:
                score += number * 0.2
            elif number >= 31 and number <= 60:
                score += number * 0.5
            else:
                score += number * 1
            return score

    # criteria: staff
    def cal_staff_score(temp, score=0):
        if temp < 36.3:
            score += (36.3 - temp) * 100
        elif temp > 37.2:
            score += (temp - 37.2) * 150

        return score

    return render(request, "?")


# Profile
@login_required
def profile(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")

    return render(request, template_name='profile.html', 
                    context={"username": username, "usertype": usertype})


# Update Profile
@login_required
def update_profile(request):
    username = request.COOKIES.get("username")

    if request.method == "POST":
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        address = request.POST['address']
        tel = request.POST['tel']

        # update criteria
        if password1 == password2:
            if_update = False
            if password1 != '':
                if_update = True
                User.objects.filter(username=username).update(password=password1)
            if address != '':
                if_update = True
                User.objects.filter(username=username).update(address=address)
            if tel != '':
                if_update = True
                User.objects.filter(username=username).update(tel=tel)
            
            if if_update:
                messages.success(request, '修改成功!')
                return redirect(reverse("dashboard:profile"))
            else:
                messages.info(request, '未输入有效信息')
                return redirect(reverse("dashboard:profile"))
        
        else:
            messages.info(request, '两次密码不同，请重新输入')
            return redirect(reverse("dashboard:update_profile"))
    
    return render(request, template_name='update_profile.html')


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


# Seller-information-summary: Search orders
@login_required
def seller_information_summary_orders(request):
    """
    Search information from orderinformation and deliveryinformation tables.
    """
    username = request.COOKIES.get("username")
    delivery_orders = DeliveryInformation.objects.filter(sno_id=username)
    delivery_filter = DeliveryFilterCompany(request.GET, queryset=delivery_orders)
    delivery_orders = delivery_filter.qs
    
    context = {
        'username': username,
        'delivery_filter': delivery_filter,
        'delivery_orders': delivery_orders,
    }
    return render(request, 'information-summary-seller.html', context)


# Platform-information-summary: Search orders
@login_required
def platform_information_summary_orders(request):
    """
    Search information from orderinformation and deliveryinformation tables.
    """
    username = request.COOKIES.get("username")
    delivery_orders = DeliveryInformation.objects.filter(order_information__platformname_id=username)
    delivery_filter = DeliveryFilterCompany(request.GET, queryset=delivery_orders)
    delivery_orders = delivery_filter.qs
    
    context = {
        'username': username,
        'delivery_filter': delivery_filter,
        'delivery_orders': delivery_orders,
    }
    return render(request, 'information-summary-platform.html', context)


# Company-information-summary: Search orders
@login_required
def company_information_summary_orders(request):
    """
    Search information from orderinformation and deliveryinformation tables.
    """
    username = request.COOKIES.get("username")
    delivery_orders = DeliveryInformation.objects.filter(tno=username)
    delivery_filter = DeliveryFilterCompany(request.GET, queryset=delivery_orders)
    delivery_orders = delivery_filter.qs
    
    context = {
        'username': username,
        'delivery_filter': delivery_filter,
        'delivery_orders': delivery_orders,
    }
    return render(request, 'information-summary-company.html', context)
