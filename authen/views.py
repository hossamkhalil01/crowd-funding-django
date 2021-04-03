from django.contrib import messages
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm


# Create your views here.
def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "authen/register.html", {"form":form})


def login (request):

    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        return redirect("home")
    return render(request, "authen/login.html",{"form": form})


def logout(request):

    dj_logout(request)
    messages.info(request , "You have successfully logged out.")
    return redirect("login")
