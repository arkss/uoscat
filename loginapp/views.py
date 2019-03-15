from django.shortcuts import render, redirect
from django.contrib.auth import logout
def login(request):
    return render(request, "loginapp/login.html")


def my_logout(request):
    logout(request)
    return redirect('/')