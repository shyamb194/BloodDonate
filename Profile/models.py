from django.db import models
from django.contrib.auth.models import User

from UserAuthentication.models import *


# Create your models here.
def upload_path(instance, filename): 
    return 'user_{0}/{1}'.format(instance.user.username, filename) 

class Post(models.Model):
	author = models.ForeignKey(ProfileDetails, null = True, on_delete=models.CASCADE)
	caption = models.CharField(max_length = 200, blank = True, null = True)
	post_type = models.CharField(max_length = 20, blank = False, null = False)
	post_audience = models.CharField(max_length = 20, blank = False, null = False)
	updated = models.DateTimeField(auto_now = True)
	created = models.DateTimeField(auto_now_add = True)

	def post_image(self):
		return self.postimage_set.all()

	class Meta:
		db_table = 'post'
		ordering = ('-created',)

class PostImage(models.Model):
	user = models.ForeignKey(User, null = False, on_delete=models.CASCADE)
	postid = models.ForeignKey(Post, null = True, on_delete = models.CASCADE)
	image = models.ImageField(upload_to = upload_path, blank = True, null = True)

	class Meta:
		db_table = 'postImage'
