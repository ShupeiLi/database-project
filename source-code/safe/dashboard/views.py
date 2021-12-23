# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import OrderInformation, DeliveryInformation
from django.urls import reverse_lazy
from django.contrib import messages
from .tools import encrypt
from .models import Health
import datetime

User = get_user_model()

# Create your views here.
# Homepage
@login_required
def board_home(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")
    return render(request, "board-home.html", 
                  context={"username": username, "usertype": usertype})

# Delivery Historical Data
@login_required
def delivery_health(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")

    health = Health.objects.order_by('-pupdate')

    context={"username": username, "usertype": usertype}

    return render(request, "delivery-health-view.html", context)

# Add New
@login_required
def addnew(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")
    
    context={"username": username, "usertype": usertype}

    return render(request, "?", context) 

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

            
            
            
            
