from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

