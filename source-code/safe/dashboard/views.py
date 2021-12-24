from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import OrderInformation, DeliveryInformation, Health, Distribution
from django.urls import reverse_lazy
from django.contrib import messages
from .tools import encrypt
from .forms import HealthForm, DistributionForm


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


# Delivery: Show recent health information of the deliveryman
@login_required
def health(request):
    health = Health.objects.all()
    context = {
        'health': health,
    }
    return render(request, 'dashboard/health.html', context)


# Delivery: Submit today's health information
@login_required
def create_health(request):
    health_form = HealthForm()
    if request.method == 'POST':
        if 'c-button' in request.POST:
            health_form = HealthForm(request.POST)
            if health_form.is_valid():
                username_get = health_form.cleaned_data['username']
                pcity_get = health_form.cleaned_data['pcity']
                ptemp_get = health_form.cleaned_data['ptemp']
                health = Health.objects.create(username=username_get, pcity=pcity_get, ptemp=ptemp_get)
                health.save()
                return redirect('health')
    context = {
        'health_form': health_form
    }
    return render(request, 'dashboard/createhealth.html', context)           
            
# Delivery: Show the order information distributed to the deliveryman
@login_required          
def distribution(request):
    distribution = Distribution.objects.all()
    distribution_count = distribution.count()
    distribution_p_count = Distribution.objects.filter(status='pending').count()
    distribution_c_count = Distribution.objects.filter(status='confirmed').count()

    context = {
        'distribution_count': distribution_count,
        'distribution_p_count': distribution_p_count,
        'distribution_c_count': distribution_c_count,
        'distribution': distribution
    }     
    return render(request, 'dashboard/distribution.html', context)

# Delivery: Confirm the order distributed to himself
@login_required   
def confirm_distribution(request, pk):
    distribution = Distribution.objects.get(id=pk)
    distribution_form = DistributionForm(instance=distribution)
    if request.method == 'POST':
        distribution_form = DistributionForm(request.POST)
        if distribution_form.is_valid():
            dpno_get = distribution_form.cleaned_data['dpno']
            dno_get = distribution_form.cleaned_data['dno']
            username_get = distribution_form.cleaned_data['username']
            status_get = distribution_form.cleaned_data['status']
            distribution = Distribution.objects.filter(id=pk)
            distribution.update(id=pk, dpno=dpno_get, dno=dno_get, username=username_get, status=status_get)
            return redirect('distribution')
    context = {
        'distribution': distribution,
        'distribution_form': distribution_form
    }
    return render(request, 'dashboard/confirmdistribution.html', context)
          