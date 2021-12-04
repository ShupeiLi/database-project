from DBUser.models import DBUser
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect


# constants
Location = {'buyer': '/buyer_main/'}


# login function
def login(request):
    ctx = {}  # context
    if request.method == 'POST' and request.POST:
        # get content from request
        usertype = request.POST.get("usertype")
        username = request.POST.get("username")
        password = request.POST.get("password")
        # define
        try:
            user = DBUser.objects.get(usertype=usertype, username=username)
        except DBUser.DoesNotExist:
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


