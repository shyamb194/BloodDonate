from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from UserAuthentication.models import *

class CreateUserForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name']

class ProfileDetailsForm(ModelForm):
	class Meta:
		model = ProfileDetails
		fields = ['gender', 'bloodGroup', 'dob', 'contact', 'bio', 'profile_pic', 'permCountry', 'permState', 'permDistrict', 'permCity', 'tempCountry', 'tempState', 'tempDistrict', 'tempCity']