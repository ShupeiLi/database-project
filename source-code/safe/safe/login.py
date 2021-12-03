import hashlib
from DBUser.models import DBUser
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
    ctx = {}
    if request.method == 'POST' and request.POST:
        usertype = request.POST.get("usertype")
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = DBUser.objects.get(usertype=usertype, username=username)
        if user:  # username == "18307100100"
            # now_password = setPassword(password)
            db_password = user.password
            if password == db_password:  # 密码正确
                response = HttpResponseRedirect('/buyer_main/')  # 跳转至新的页面
                response.set_cookie("username", username)  #
                return response
            else:  # 密码错误
                ctx['rlt'] = "用户或密码错误！"

    return render(request, "login.html", ctx)


