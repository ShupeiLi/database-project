# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

# Create your views here.
# Homepage
def board_home(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")
    return render(request, "board-home.html", 
                  context={"username": username, "usertype": usertype})

# Profile
def profile(request):
    return render(request, 'profile.html')

# User Profile
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
                messages.info(request, '修改成功!')
                return redirect(reverse("dashboard:update_profile"))
            else:
                return redirect(reverse("dashboard:update_profile"))
        
        else:
            messages.info(request, '两次密码不同，请重新输入')
            return redirect(reverse("dashboard:update_profile"))
    
    return render(request, template_name='update_profile.html')
