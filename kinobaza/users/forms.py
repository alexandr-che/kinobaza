from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')