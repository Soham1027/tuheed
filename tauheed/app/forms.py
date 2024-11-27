import re
from django import forms
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm


class UserDataRegisterForm(UserCreationForm):
    class Meta:
        model = UserData
        fields = [
            'first_name', 'last_name', 'username', 'email', 'gender', 'date_of_birth', 
            'parent_name', 'parent_phone_number', 'parent_surname', 'school_college_or_employment',
            'diversity', 'photo_consent', 'term_and_condition_gdpr'
        ]
        
    # Additional validation for password confirmation can be handled by the UserCreationForm
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

# Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class AddStaffForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = UserData
        fields = ['first_name','username', 'last_name', 'email', 'password', 'is_active']

    def save(self, commit=True):
        staff = super().save(commit=False)
        staff.password = make_password(self.cleaned_data['password'])  # Hash the password here
        if commit:
            staff.save()
        return staff