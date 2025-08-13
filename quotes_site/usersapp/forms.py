from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"required": True}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"required": True}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"required": True}))

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


# Аватар
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            max_size = 5 * 1024 * 1024  # 5 Мб
            if avatar.size > max_size:
                raise ValidationError("Image file too large ( > 5MB )")
        return avatar
