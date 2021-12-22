from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import OrderInformation, DeliveryInformation
from django.urls import reverse_lazy
from django.contrib import messages


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
        if OrderInformation.objects.filter(ono=request.POST.get('ono')).exists():
            ono = OrderInformation.objects.get(ono=request.POST.get('ono')).ono
            selected_company = get_object_or_404(User, username=request.POST.get('tno'))
            tno = selected_company.tno
            dtrans = request.POST.get('dtrans')
            new_delivery = DeliveryInformation.objects.create_deliveryinfo_seller(ono, dtrans, tno, sno)
            new_delivery.save()
            return HttpResponseRedirect(reverse_lazy("dashboard:boardhome"))
        else:
            messages.info(request, "请输入有效订单号")
    
    return render(request, "seller-order-submit.html", 
                  context={'companys':companys, "username": sno})

            
            
            
            