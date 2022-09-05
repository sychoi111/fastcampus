from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm

User = get_user_model()


def index(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")

            user = authenticate(username = username, password = raw_password)
            if user is not None:
                msg = "로그인 성공하였습니다."
                login(request, user)
            return redirect('/')					
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)						
    return HttpResponseRedirect("/")


@login_required
def user_list_view(request):
    users = User.objects.order_by("id").all()
    paginator = Paginator(users, 3)
    page = request.GET.get('page')
    user = paginator.get_page(page)
    return render(request, "users.html", {"users": user})
