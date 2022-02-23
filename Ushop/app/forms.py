from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.core import validators
from django.utils.translation import gettext, gettext_lazy


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", help_text="at least 5 characters",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password Again",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email", validators=[validators.MaxLengthValidator(30)],
                            required=True, label_suffix=":", initial="somthing@email.com",
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=gettext_lazy('Password'), strip=False,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                                                 'class': 'form-control'}))