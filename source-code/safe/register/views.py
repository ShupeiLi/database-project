# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.hashers import check_password


User = get_user_model()

# Register view function
def register(request):

	if request.method == "POST":
		# get info from user
		username = request.POST['username']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		utype = request.POST['utype']
		companyname = request.POST['companyname']
		address = request.POST['address']
		tel = request.POST['tel']
		email = request.POST['email']
        
        # Individual company name
		if utype == "buyer" or utype == "seller" or utype == "delivery":
			companyname = "Individual"
        
		# check blank
		if not username:
			messages.info(request, '必须输入用户名')
			return redirect(reverse("register:signup"))
		if not password1:
			messages.info(request, '必须输入有效密码')
			return redirect(reverse("register:signup"))
		if not password2:
			messages.info(request, '必须确认密码')
			return redirect(reverse("register:signup"))
		if not utype:
			messages.info(request, '必须填写用户类型')
			return redirect(reverse("register:signup"))
		if not companyname:
			messages.info(request, '必须输入公司名')
			return redirect(reverse("register:signup"))
		if not email:
			messages.info(request, '必须提供邮箱')
			return redirect(reverse("register:signup"))

		# register criteria
		if password1 == password2:
			if User.objects.filter(username=username).exists():
				messages.info(request, '用户名已存在')
				return redirect(reverse("register:signup"))
			elif User.objects.filter(email=email).exists():
				messages.info(request, '邮箱已使用')
				return redirect(reverse("register:signup"))
			else:
				user = User.objects.create_user(username=username, password=password1, utype=utype, 
                                                companyname=companyname, address=address, tel=tel, email=email)					
				user.save()
				messages.info(request, '注册成功!')
                
		else:
			messages.info(request, '密码不正确!')
			return redirect(reverse("register:register"))
	
		return redirect(reverse("register:login"))

	return render(request=request, template_name='register.html')


# Login view function
def login(request):
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
            if user.is_active:
                if check_password(password, user.password):  # 密码正确
                    response = HttpResponseRedirect(reverse_lazy("dashboard:boardhome"))  # 跳转至新的页面
                    response.set_cookie("username", username)  # 设置cookie
                    response.set_cookie("usertype", usertype)
                    return response
                else:  # 密码错误显示提醒
                    messages.info(request, '密码不正确!')
            else: # 账户未激活错误
                messages.info(request, "账户未激活，请通过邮件链接激活账户！")
        else:  # 用户名或类别显示提醒
            messages.info(request, "用户名或类别错误！")

    return render(request=request, template_name="login.html")


# Home page view function
def home(request):
    """
    Define home page view. Template: home.html
    
    Returns:
        home_page_view
    """
    return render(request, "home.html")