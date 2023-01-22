from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts/register.html")

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name)
        return redirect("accounts:login_view")


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts/login.html")

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home:meeting_view")
        else:
            return redirect("accounts:login_view")