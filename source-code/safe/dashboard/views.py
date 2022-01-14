# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from .models import OrderInformation, DeliveryInformation, RateSeller, RateDelivComp, HealthInformation, DistributionInformation, CompanyStaff, GeographicInformation, PandemicInformation, GeographicTransformation
from django.urls import reverse_lazy
from django.contrib import messages
from .tools import encrypt
from .filters import DeliveryFilter, SellerRatingFilter, CompanyRatingFilter
import datetime


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

    health = HealthInformation.objects.filter(pno_id=username).order_by('-pupdate')

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
        
        if HealthInformation.objects.filter(pno_id=username).filter(pupdate=datetime.date.today()).exists():
            messages.warning(request, '今日已填写')
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


# Profile
@login_required
def profile(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")

    if request.method == 'POST':
        logout(request)
        return redirect(reverse_lazy("register:login"))

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
                return redirect(reverse_lazy("register:login"))
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
        order = DeliveryInformation.objects.filter(tno_id = username).filter(is_checked=True)
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

         
# Delivery: Confirm the order distribution
@login_required          
def delivery_distribution_homepage(request):
    username = request.COOKIES.get("username")
    distribution = DistributionInformation.objects.filter(pno_id=username)
    distribution_count = distribution.count()
    distribution_p_count = DistributionInformation.objects.filter(pno_id=username).filter(is_checked=False).count()
    distribution_c_count = DistributionInformation.objects.filter(pno_id=username).filter(is_checked=True).count()

    if request.method == 'POST':
        confirm_distribution_id = request.POST.get('confirm')
        comfirm_dpno = confirm_distribution_id + username
        confirm_distribution = DistributionInformation.objects.get(dpno = comfirm_dpno) 
        confirm_distribution.is_checked = True
        confirm_distribution.save()
        return redirect(reverse("dashboard:delivery-distribution-home"))

    context = {
        'distribution_count': distribution_count,
        'distribution_p_count': distribution_p_count,
        'distribution_c_count': distribution_c_count,
        'distribution': distribution,
        'username': username,
    }     
    return render(request, 'delivery-distribution-home.html', context)


# Buyer-information-summary: Search orders
@login_required
def buyer_information_summary_orders(request):
    """
    Search information from orderinformation and deliveryinformation tables.
    """
    username = request.COOKIES.get("username")
    delivery_orders = DeliveryInformation.objects.filter(buyer_id=username)
    delivery_filter = DeliveryFilter(request.GET, queryset=delivery_orders)
    delivery_orders = delivery_filter.qs
    
    context = {
        'username': username,
        'delivery_filter': delivery_filter,
        'delivery_orders': delivery_orders,
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
    delivery_filter = DeliveryFilter(request.GET, queryset=delivery_orders)
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
    delivery_filter = DeliveryFilter(request.GET, queryset=delivery_orders)
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
    delivery_filter = DeliveryFilter(request.GET, queryset=delivery_orders)
    delivery_orders = delivery_filter.qs
    
    context = {
        'username': username,
        'delivery_filter': delivery_filter,
        'delivery_orders': delivery_orders,
    }
    return render(request, 'information-summary-company.html', context)


# Buyer: Seller Scores
@login_required
def buyer_view_seller_scores(request):
    """
    Search seller scores.
    """
    username = request.COOKIES.get("username")
    seller_ratings = RateSeller.objects.all()
    seller_filter = SellerRatingFilter(request.GET, queryset=seller_ratings)
    seller_ratings = seller_filter.qs

    context = {
        'username': username,
        'seller_filter': seller_filter,
        'seller_ratings': seller_ratings,
    }
    return render(request, 'score-buyer.html', context)


# Platform: Seller Scores
@login_required
def platform_view_seller_scores(request):
    """
    Search seller scores.
    """
    username = request.COOKIES.get("username")
    seller_ratings = RateSeller.objects.all()
    seller_filter = SellerRatingFilter(request.GET, queryset=seller_ratings)
    seller_ratings = seller_filter.qs

    context = {
        'username': username,
        'seller_filter': seller_filter,
        'seller_ratings': seller_ratings,
    }
    return render(request, 'score-platform.html', context)


# Seller: Company Scores
@login_required
def seller_view_company_scores(request):
    """
    Search company scores.
    """
    username = request.COOKIES.get("username")
    company_ratings = RateDelivComp.objects.all()
    company_filter = CompanyRatingFilter(request.GET, queryset=company_ratings)
    company_ratings = company_filter.qs
    
    context = {
        'username': username,
        'company_filter': company_filter,
        'company_ratings': company_ratings,
    }
    
    return render(request, 'score-seller.html', context)


# Company: Manage delivery staffs
@login_required
def company_manage_staffs(request):
    """
    Delivery staffs' information summary.
    """
    username = request.COOKIES.get("username")
    staffs = CompanyStaff.objects.filter(tno_id=username)
    
    
    context = {
        'username': username,
        'staffs': staffs,
    }
    
    return render(request, 'company-manage-staffs.html', context)


# Company: View the health history
@login_required
def company_staff_history(request, pno):
    """
    View the health history.
    """
    username = request.COOKIES.get("username")
    pno = pno.replace("-", " ").title()
    records = HealthInformation.objects.filter(pno_id=pno).order_by('-pupdate')

    context = {
        'username': username,
        'records': records,
    }
    
    return render(request, 'company-staff-history.html', context)


# Company: View the order distribution
@login_required
def company_view_order_distribution(request, dno):
    """
    View the order distribution.
    """
    username = request.COOKIES.get("username")
    records = DistributionInformation.objects.filter(dno_id=dno)

    context = {
        'username': username,
        'records': records,
    }
    
    return render(request, 'company-view-order-distribution.html', context)

  
# Path visualization
@login_required
def visualiztion(request, orderid):
    """
    Path visualiztion.
    """
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")
    delivery_id = str(orderid).rjust(6, '0')
    d_info = DeliveryInformation.objects.get(dno=delivery_id)
    dot_list = GeographicInformation.objects.filter(dno=delivery_id)
    if request.method == 'POST':
        selected_option = request.POST.get("search_date")
        sel_time = request.POST.get("search_date").split("-")
        province_covid = PandemicInformation.objects.filter(date__contains=datetime.date(int(sel_time[0]), int(sel_time[1]), int(sel_time[2])))
    else:
        selected_option = str(d_info.dsetime)
        default_time = str(d_info.dsetime).split("-")
        province_covid = PandemicInformation.objects.filter(
            date__contains=datetime.date(int(default_time[0]), int(default_time[1]), int(default_time[2])))
    # province_covid = PandemicInformation.objects.filter(date__range=[d_info.dsetime, d_info.dretime])
    heatmapdata = []  # ('北京市','#FFFF00')
    place = []
    for x in province_covid:
        province = x.place
        if province not in place:
            place.append(province)
            # number = int(x.number)
            number = sum([int(x.number) for i in range(len(province_covid)) if province_covid[i].place == province])
            if number >= 50:
                color = '#ff9900'
            elif number > 0:
                color = '#FFFF00'
            heatmapdata.append((province, color))
    path_dot = []
    # path_dot = [("112.368904","39.913423"), ("116.382122","39.901176"), ("116.387271","39.912501"), ("118.398258","39.904600")]
    for i in range(len(dot_list)):
        loc = dot_list[i].dloc
        latlon = loc.split(",")
        lon = latlon[0]
        lat = latlon[1]
        path_dot.append((float(lat), float(lon)))

    time_list = []
    i = d_info.dsetime
    while i <= d_info.dretime:
        time_list.append(str(i))
        i = i + datetime.timedelta(days=1)
    context = {
        "username": username,
        "usertype": usertype,
        "heatmapdata": heatmapdata,
        "path_dot": path_dot,
        "center": path_dot[-1],
        "time_list": time_list,
        "selected_option": selected_option
        }

    return render(request, "visualiztion.html", context)


# Logistics risk
@login_required
def logistics_risk(request, orderid):
    """
    Risk esitimation.
    """
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")
    
    # delivery district risk score
    records = GeographicInformation.objects.filter(dno=orderid)
    pandemic_records = PandemicInformation.objects.all()
    district_count = 0
    district_check = False
    
    for record in records:
        record_date = record.dupdate
        record_loc = record.dloc.split(",")
        record_lat = float(record_loc[0])
        record_lng = float(record_loc[1])
        
        for pandemic_record in pandemic_records:
            pandemic_record_date = pandemic_record.date
            if (record_date.date() - pandemic_record_date.date()).days == 0:
                transform_record1 = GeographicTransformation.objects.filter(dpro=pandemic_record.place)
                transform_record2 = GeographicTransformation.objects.filter(dloc=pandemic_record.place)
                check = False
                if len(transform_record1) != 0:
                    pandemic_record_lat = float(transform_record1[0].dlat)
                    pandemic_record_lng = float(transform_record1[0].dlng)
                    check = True
                if len(transform_record2) != 0:
                    pandemic_record_lat = float(transform_record2[0].dlat)
                    pandemic_record_lng = float(transform_record2[0].dlng)                
                    check = True
                if check:
                    distance = (pandemic_record_lat - record_lat) ** 2 + (pandemic_record_lng - record_lng)  ** 2
                    if distance <= 2:
                        district_count += 1
    if len(records) == 0:
        district_risk_score = 0
        district_check = True
    else:
        district_risk_score = (district_count / len(records)) * 10
    
    # delivery staff risk score
    if DeliveryInformation.objects.filter(dno=orderid).exists():
        staff_check = False
        delivery_record = DeliveryInformation.objects.get(dno=orderid)
        dsetime = delivery_record.dsetime
        dretime = delivery_record.dretime
        delivery_staffs = DistributionInformation.objects.filter(dno_id=orderid)
        temp_count = 0
        temp_total = 0
        
        for delivery_staff in delivery_staffs:
            health_records = HealthInformation.objects.filter(pno_id=delivery_staff.pno_id, pupdate__range=(dsetime, dretime))
            if len(health_records) != 0:
                for health_record in health_records:
                    if float(health_record.ptemp) > 37.2:
                        temp_count += 1
            temp_total += len(health_records)
        
        if temp_total != 0:        
            staff_risk_score = (temp_count / temp_total) * 10
        else:
            staff_risk_score = 0
            staff_check = True
    else:
        staff_risk_score = 0
        staff_check = True
    
    risk_score = 0.2 * district_risk_score + 0.8 * staff_risk_score
    
    if district_check and staff_check:
        con = "该订单暂时没有对应的物流信息"
    else:
        con = ""
    
    context = {
        "username": username,
        "usertype": usertype,
        "orderid": orderid,
        "district": "{:.3f}".format(district_risk_score),
        "staff": "{:.3f}".format(staff_risk_score),
        "total": "{:.3f}".format(risk_score),
        "con": con,
        }    
    
    return render(request, "risk.html", context)