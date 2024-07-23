from django import forms
# Django's forms:
# used to handle user input and validate data submitted through HTML forms.
# to create, update, and validate data before saving it to the database

from django.contrib.auth.models import User
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    # age = forms.IntegerField() --> simple line like this doesn't add the data into the database. We gotta use AbstractUser

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    # to check password and conform password. Not stored in database, but used for checking
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

from django.contrib.auth.forms import AuthenticationForm
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
"""
Default Djangos field possible
--------------------------------------------------------------
username
password
email
first_name
last_name
is_staff
is_active
date_joined
last_login
groups
user_permissions
--------------------------------------------------------------
"""
from .models import Product
class ProductRegistrationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

from .models import Review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']