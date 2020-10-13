from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User


from Profile.models import *

# Create your views here.
def home(request):
	context = {}
	return render(request, 'Home/home.html', context)

def whoCandonateBlood(request):
	context = {}
	return render(request, 'Home/whoCandonateBlood.html', context)

def newsFeed(request):
	user_posts = Post.objects.filter(post_audience = 'public')
	context = {
			'post': user_posts
			}
	return render(request, 'Home/newsFeed.html', context)

def newsAndEvents(request):
	context = {}
	return render(request, 'Home/newsAndEvents.html', context)

