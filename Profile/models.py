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
	like = models.ManyToManyField(User, related_name = 'like', blank = True)
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

class Comments(models.Model):
	post = models.ForeignKey(Post, null = True, related_name = "comments", on_delete=models.CASCADE)
	user = models.ForeignKey(User, null = True, on_delete=models.CASCADE)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'comments'
		ordering = ('created',)

class ReplyComments(models.Model):
	comment = models.ForeignKey(Comments, related_name = "replyComments", null = True, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, null = True, on_delete=models.CASCADE)
	user = models.ForeignKey(User, null = True, on_delete=models.CASCADE)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'replyComments'
		ordering = ('created',)

class Notifications(models.Model):
	NOTIFICATION_TYPE = ((1,'CreatePost'),(2,'Like'),(3,'Comment'),(4,'Follow'))
	post = models.ForeignKey(Post, null = True, blank = True, on_delete=models.CASCADE, related_name = "noti_post")
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "noti_from_user")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "noti_to_user")
	notification_type = models.IntegerField(choices = NOTIFICATION_TYPE)
	text_preview = models.CharField(max_length = 90, blank = True)
	date = models.DateTimeField(auto_now_add = True)
	is_seen = models.BooleanField(default = False)

	class Meta:
		db_table = 'Notification'
