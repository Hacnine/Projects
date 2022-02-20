from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", help_text="at least 5 characters",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password Again",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email", required=True, label_suffix=":", initial="somtehing@email.com",
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}
