import re
from django import forms
from django.core.exceptions import ValidationError
from app.models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=4)
    continue_ = forms.CharField(widget=forms.HiddenInput(), initial='index')


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    continue_ = forms.CharField(widget=forms.HiddenInput(), initial='login')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

    def clean_username(self):
        pattern = r'^[a-zA-Z0-9_]+$'
        data = self.cleaned_data['username']

        if not re.match(pattern, data):
            raise ValidationError('Try another username for login')
        return data

    def clean_email(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        data = self.cleaned_data['email']
        if not re.match(pattern, data):
            raise ValidationError('Invalid email')
        return data

    def clean_password_check(self):
        if not self.cleaned_data['password_check'] == self.cleaned_data['password']:
            raise ValidationError('Passwords are different')

    def clean_first_name(self):
        pattern = r'^[a-zA-Z]+$'
        data = self.cleaned_data['first_name']
        if not re.match(pattern, data):
            raise ValidationError('Try another nickname')


class AskForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['title']

    text = forms.CharField(widget=forms.Textarea)
    tags_ = forms.CharField(required=False)
