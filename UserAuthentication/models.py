from django.db import models
from django.contrib.auth.models import User

from Profile.models import *
# Create your models here.

class ProfileDetails(models.Model):
	gender_choice = (
			('Male', 'Male'),
			('Female', 'Female'),
			('Others', 'Others')
		)
	bloodGroup_choice = (
			('A+', 'A+'),
			('B+', 'B+'),
			('AB+', 'AB+'),
		)
	stateChoice = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'))

	user = models.OneToOneField(User, null = False, on_delete=models.CASCADE)
	following = models.ManyToManyField(User, related_name = 'following', blank = True)
	gender = models.CharField(max_length = 20, blank = False, null = False, choices = gender_choice)
	bloodGroup = models.CharField(max_length = 20, blank = False, null = False, choices = bloodGroup_choice)
	dob = models.DateField(auto_now=False, auto_now_add=False)
	contact = models.CharField(max_length = 20, blank = False, null = False)
	contact_audience = models.CharField(max_length = 20, blank = False, null = False)
	bio = models.TextField(max_length=200, blank = True, null = True)
	profile_pic = models.ImageField(default = '/images/defaultProfilePic.png')
	last_donated = models.DateField(auto_now = True)

	permCountry = models.CharField(max_length = 30, blank = False, null = False)
	permState = models.CharField(max_length = 30, blank = False, null = False, choices = stateChoice)
	permDistrict = models.CharField(max_length = 30, blank = False, null = False)
	permCity = models.CharField(max_length = 30, blank = False, null = False)

	tempCountry = models.CharField(max_length = 30, blank = False, null = False)
	tempState = models.CharField(max_length = 30, blank = False, null = False, choices = stateChoice)
	tempDistrict = models.CharField(max_length = 30, blank = False, null = False)
	tempCity =models.CharField(max_length = 30, blank = False, null = False)

	updated = models.DateTimeField(auto_now = True)
	created = models.DateTimeField(auto_now_add = True)

	def profiles_post(self):
		return self.post_set.all()

	def following_count(self):
		return self.following.count()

	class Meta:
		db_table = 'profielDetails'
		ordering = ('-created',)

