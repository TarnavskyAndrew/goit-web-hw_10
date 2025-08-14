from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile


# форма регістрації 
class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"required": True}))  
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"required": True}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"required": True}))

    # для валідації
    class Meta:
        model = User # модель користувача
        fields = ["username", "password1", "password2"] # поля для реєстрації


# форма авторизації
class LoginForm(AuthenticationForm):
    
    # поля для авторизації
    class Meta:
        model = User # модель користувача
        fields = ["username", "password"]


# форма для редагування профілю користувача
class ProfileForm(forms.ModelForm):
    
    # поле для аватарки
    class Meta:
        model = Profile  # модель профілю
        fields = ["avatar"] # поля для редагування профілю   
 
    # валідація аватарки
    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar") # отримуємо аватарку з даних форми
        if avatar: # якщо аватарка не порожня
            # перевіряємо розмір файлу аватарки
            max_size = 5 * 1024 * 1024  # 5 Мб  
            # якщо розмір аватарки більший за максимальний розмір
            if avatar.size > max_size:   
                raise ValidationError("Image file too large ( > 5MB )")
        return avatar
