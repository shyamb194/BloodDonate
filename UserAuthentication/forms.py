from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['email', 'username', 'password1', 'password2', 'first_name', 'last_name']

class ProfileDetailsForm(ModelForm):
	class Meta:
		model = ProfileDetails
		fields = ['gender', 'bloodGroup', 'dob', 'contact', 'bio', 'profile_pic', 'permCountry', 'permState', 'permDistrict', 'permCity', 'tempCountry', 'tempState', 'tempDistrict', 'tempCity']