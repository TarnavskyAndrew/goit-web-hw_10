from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .forms import ProfileForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("quotes:index")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created. Please login.")
            login(request, user)  # автологiн
            return redirect("quotes:index")
        return render(request, "usersapp/signup.html", {"form": form})
    return render(request, "usersapp/signup.html", {"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect("quotes:index")
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user is None:
            messages.error(request, "Username or password didn't match")
            return redirect("users:login")
        login(request, user)
        next_url = request.GET.get("next", None)
        return redirect(next_url or "quotes:index")
    return render(request, "usersapp/login.html", {"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect("quotes:index")


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("quotes:index")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "usersapp/profile_edit.html", {"form": form})

