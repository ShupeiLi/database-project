from django.shortcuts import render
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your views here.
# Homepage
def board_home(request):
    username = request.COOKIES.get("username")
    usertype = request.COOKIES.get("usertype")
    return render(request, "board-home.html", 
                  context={"username": username, "usertype": usertype})
