from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Developer, MaintenanceProvider, Technician, AccountType

# User registration form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    account_type = forms.ChoiceField(choices=[(tag, tag.value) for tag in AccountType])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'account_type', 'password1', 'password2']

# Login form
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
