from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
import re


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control registration-form', 'placeholder': 'Create password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control registration-form', 'placeholder': 'Create username'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control registration-form', 'placeholder': 'Paste your email'})
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        return password



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'password', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'username', 'autocomplete': 'off'}))


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'


class FileSharingForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter the email address',
        })
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your message. \n\nThe link will be attached automatilally at the end of this message', "class": "email-text-input",
        })
    )
