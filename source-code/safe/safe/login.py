import hashlib
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect


def setPassword(password):
    """
    加密密码，算法单次md5
    :param apssword: 传入的密码
    :return: 加密后的密码
    """
    md5 = hashlib.md5()
    md5.update(password.encode())
    password = md5.hexdigest()
    return str(password)


def login(request):
    if request.method == 'POST' and request.POST:
        userType = request.POST.get("userType")
        username = request.POST.get("username")
        password = request.POST.get("password")
        # e = OAUser.objects.filter(email=email).first()
        if e:
            now_password = setPassword(password)
            db_password = e.password
            if now_password == db_password:
                response = HttpResponseRedirect('/index/')
                response.set_cookie("username", e.username)
                return response

    return render(request, "login.html")


