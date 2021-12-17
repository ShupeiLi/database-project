# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse


User = get_user_model()
# constants
Location = {'buyer': '/buyer_main/'}

# Register view function
def register(request):

	if request.method == "POST":
		# get info from user
		username = request.POST['username']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		utype = request.POST['utype']
		companyname = request.POST['companyname']
		registerid = request.POST['registerid']
		address = request.POST['address']
		tel = request.POST['tel']
		email = request.POST['email']

		# check blank
		if not username:
			messages.info(request, 'You must provide a username')
			return redirect(reverse("register:register"))
		if not password1:
			messages.info(request, 'You must provide a valid password')
			return redirect(reverse("register:register"))
		if not password2:
			messages.info(request, 'You must confirm your password')
			return redirect(reverse("register:register"))
		if not utype:
			messages.info(request, 'You must provide a user type')
			return redirect(reverse("register:register"))
		if not companyname:
			messages.info(request, 'You must provide a companyname')
			return redirect(reverse("register:register"))
		if not registerid:
			messages.info(request, 'You must provide a registerid')
			return redirect(reverse("register:register"))
		if not email:
			messages.info(request, 'You must provide an email')
			return redirect(reverse("register:register"))

		# register criteria
		if password1 == password2:
			if User.objects.filter(username=username).exists():
				messages.info(request, 'Username taken')
				return redirect(reverse("register:register"))
			elif User.objects.filter(email=email).exists():
				messages.info(request, 'Email taken')
				return redirect(reverse("register:register"))
			elif User.objects.filter(registerid=registerid).exists():
				messages.info(request, 'Register ID taken')
				return redirect(reverse("register:register"))
			else:
				user = User.objects.create_user(username=username, password=password1, utype=utype, companyname=companyname, 
        										registerid=registerid, address=address, tel=tel, email=email)
				user.save()
				messages.info(request, 'Registration successful!')
                
		else:
			messages.info(request, 'Password not matching!')
			return redirect(reverse("register:register"))
	
		return redirect(reverse("register:login"))

	return render(request=request, template_name='register.html')


# Login view function
def login(request):
    ctx = {}  # context
    if request.method == 'POST' and request.POST:
        # get content from request
        usertype = request.POST.get("usertype")
        username = request.POST.get("username")
        password = request.POST.get("password")
        # define
        try:
            user = User.objects.get(utype=usertype, username=username)
        except User.DoesNotExist:
            user = None
        if user:
            db_password = user.password
            if password == db_password:  # 密码正确
                response = HttpResponseRedirect(Location[usertype])  # 跳转至新的页面
                response.set_cookie("username", username)  # 设置cookie
                return response
            else:  # 密码错误显示提醒
                ctx['rlt'] = "密码错误！"
        else:  # 用户名或类别显示提醒
            ctx['rlt'] = "用户名或类别错误！"

    return render(request, "login.html", ctx)


# Home page view function
def home(request):
    """
    Define home page view. Template: home.html
    
    Returns:
        home_page_view
    """
    return render(request, "home.html")


# Buyer main page view
def buyer(request):
    return HttpResponse("Hello, buyer")

