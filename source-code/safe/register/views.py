# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, get_user_model

User = get_user_model()

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
		# agreement = request.POST['False']

		# check blank
		if not username:
			messages.info(request, 'You must provide a username')
			return redirect('/register/')
		if not password1:
			messages.info(request, 'You must provide a valid password')
			return redirect('/register/')
		if not password2:
			messages.info(request, 'You must confirm your password')
			return redirect('/register/')
		if not utype:
			messages.info(request, 'You must provide a user type')
			return redirect('/register/')
		if not companyname:
			messages.info(request, 'You must provide a companyname')
			return redirect('/register/')
		if not registerid:
			messages.info(request, 'You must provide a registerid')
			return redirect('/register/')
		if not email:
			messages.info(request, 'You must provide an email')
			return redirect('/register/')

		# register criteria
		if password1 == password2:
			if User.objects.filter(username=username).exists():
				messages.info(request, 'Username taken')
				return redirect('/register/')
			elif User.objects.filter(email=email).exists():
				messages.info(request, 'Email taken')
				return redirect('/register/')
			elif User.objects.filter(registerid=registerid).exists():
				messages.info(request, 'Register ID taken')
				return redirect('/register/')
			else:
				user = User.objects.create_user(username=username, password=password1, utype=utype, companyname=companyname, 
										registerid=registerid, address=address, tel=tel, email=email)
				user.save();
				messages.info(request, 'Success!')
		else: 
			messages.info(request, 'Password not matching!')
			return redirect('/register/')
	
		return redirect('/')

	return render (request=request, template_name='register.html')