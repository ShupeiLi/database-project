from django.shortcuts import render
from django.http import HttpResponse


def buyer(request):
    return HttpResponse("Hello, buyer")
