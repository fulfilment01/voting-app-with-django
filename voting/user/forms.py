from django import forms 
from .models import User
from votingapp.models import Profile
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name','gender','email', 'matric', 'username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model= User
        fields=['username', 'department', 'full_name', 'email', 'matric', 'image']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields=['address', 'phonenumber']
