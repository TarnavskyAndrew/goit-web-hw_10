from django.urls import path
from . import views

app_name = "users" # Ім'я простору додатку для уникнення конфліктів URL

# URL-шляхи для додатку користувачів

urlpatterns = [
    path("signup/", views.signup, name="signup"),  # реєстрація користувача
    path("login/", views.loginuser, name="login"), # вхід користувача
    path("logout/", views.logoutuser, name="logout"), # вихід користувача
    path("profile/edit/", views.profile_edit, name="profile_edit"), # редагування профілю користувача
]
