from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .forms import ProfileForm


# функція для реєстрації користувача
def signup(request):
    if request.user.is_authenticated: # якщо користувач вже увійшов, перенаправляємо на головну сторінку
        return redirect("quotes:index")
    if request.method == "POST": # якщо метод POST, обробляємо форму реєстрації
        form = RegisterForm(request.POST)  # створюємо форму з даними POST
        if form.is_valid(): # якщо форма валідна, зберігаємо користувача
            user = form.save()  
            messages.success(request, "Account created. Please login.") # повідомлення про успішну реєстрацію
            login(request, user)  # автологiн
            return redirect("quotes:index") # перенаправляємо на головну сторінку
        return render(request, "usersapp/signup.html", {"form": form}) # якщо форма не валідна, повертаємо її з помилками
    return render(request, "usersapp/signup.html", {"form": RegisterForm()}) 


# функція для входу користувача
def loginuser(request):
    if request.user.is_authenticated: # якщо користувач вже увійшов, перенаправляємо на головну сторінку
        return redirect("quotes:index")
    if request.method == "POST": # якщо метод POST, обробляємо форму входу
        user = authenticate(  # автентифікація користувача
            username=request.POST.get("username"), password=request.POST.get("password")  
        )
        if user is None: # якщо користувач не знайдений, показуємо повідомлення про помилку
            messages.error(request, "Username or password didn't match") 
            return redirect("users:login")  # перенаправляємо на сторінку входу
        login(request, user) # виконуємо вхід користувача
        next_url = request.GET.get("next", None) # отримуємо URL для перенаправлення після входу
        return redirect(next_url or "quotes:index") # перенаправляємо на головну сторінку або на URL з параметра next
    return render(request, "usersapp/login.html", {"form": LoginForm()})


# функція для виходу користувача з системи
@login_required
def logoutuser(request):
    logout(request) # виконуємо вихід користувача
    return redirect("quotes:index")  


# функція для перегляду профілю користувача
@login_required
def profile_edit(request): 
    profile = request.user.profile # отримуємо профіль користувача
    if request.method == "POST":  # якщо метод POST, обробляємо форму редагування профілю
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # створюємо форму з даними POST та профілем користувача
        if form.is_valid(): # якщо форма валідна, зберігаємо зміни
            form.save()
            return redirect("quotes:index")
    else:
        form = ProfileForm(instance=profile) # якщо метод GET, створюємо форму з профілем користувача
    return render(request, "usersapp/profile_edit.html", {"form": form})  

