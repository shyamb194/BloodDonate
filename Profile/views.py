from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from itertools import chain

from UserAuthentication.models import *
from .models import *
from .forms import *
# Create your views here.

def sendNotifiaction(request, post):	
	followed_by = ProfileDetails.objects.filter(following = request.user)
	mail_subject = 'New post created by' + ' ' + request.user.first_name
	message = render_to_string('Profile/postNotificationEmail.html', {
			'post' : post.id,
			'domain': get_current_site(request).domain,
		})
	to_email = [user.user.email for user in followed_by]
	email = EmailMessage(mail_subject, message, request.user.email, to_email)
	email.content_subtype = "html"
	email.send(fail_silently=False)
	return redirect('UserAuthentication_app:login')


@login_required(login_url='UserAuthentication_app:login')
def follow_unfollow(request, username):
	user1 = User.objects.get(username = username)
	my_profile = ProfileDetails.objects.select_related('user').get(user = request.user.id)
	profile = ProfileDetails.objects.select_related('user').get(user = user1.id)
	if profile.user in my_profile.following.all():
		my_profile.following.remove(profile.user)
	else:
		my_profile.following.add(profile.user)
		Notifications.objects.create(
				sender = request.user,
				user = profile.user,
				notification_type = 4,
			)
	return redirect('profile_app:profileTimeline', username = username)


@login_required(login_url='UserAuthentication_app:login')
def profileTimeline(request, username):
	user1 = User.objects.get(username = username)	
	my_profile = ProfileDetails.objects.get(user = request.user)
	profile = ProfileDetails.objects.get(user = user1.id)
	followed_by = ProfileDetails.objects.filter(following = user1.id)

	try:
		notifications = Notifications.objects.filter(notification_type = 4, sender = user1).order_by('-date')
		for notifications in notifications:
			notifications.is_seen = 1
			notifications.save()
	except: 
		pass
	
	users = [user for user in my_profile.following.all()]
	posts = []
	qs = None
	if user1 in users:
		user_profile_posts = profile.post_set.exclude(post_audience = 'private')
	else:
		user_profile_posts = profile.post_set.filter(post_audience = 'public')

	for user in users:
		p =ProfileDetails.objects.get(user = user)
		p_posts = p.post_set.exclude(post_audience = 'private')
		posts.append(p_posts)
	my_post = my_profile.post_set.all()
	posts.append(my_post)	
	if len(posts) > 0:
		qs = sorted(chain(*posts), reverse = True, key = lambda obj: obj.created)
	if profile.user in my_profile.following.all():
		follow = True
	else:
		follow = False


	createUserForm = CreateUserForm(instance = user1)
	profileDetailsForm = ProfileDetailsForm(instance = profile)
	context = {
		'user': profile,
		'my_profile': my_profile,
		'my_profile_posts': qs,
		'user_profile_posts': user_profile_posts,
		'createUserForm': createUserForm,
		'profileDetailsForm': profileDetailsForm,
		'follow': follow,
		'followed_by': followed_by,
	}
	return render(request, 'Profile/profile.html', context)

@login_required(login_url='UserAuthentication_app:login')
def updateProfile(request, username):
	user1 = User.objects.get(username = username)	
	user = ProfileDetails.objects.select_related('user').get(user = user1.id)
	createUserForm = CreateUserForm(instance = user1)
	profileDetailsForm = ProfileDetailsForm(instance = user)
	if request.method == 'POST':
		createUserForm = CreateUserForm(request.POST, instance = user1)
		profileDetailsForm = ProfileDetailsForm(request.POST, instance = user)
		if createUserForm.is_valid() and profileDetailsForm.is_valid():
			createUserForm.save()
			profileDetailsForm.save()
	return redirect('profile_app:profileTimeline', username = username)


@login_required(login_url='UserAuthentication_app:login')
def createPost(request, username):
	user = User.objects.get(username = username)
	author = ProfileDetails.objects.select_related('user').get(user = user.id)
	if request.method == 'POST':
		caption = request.POST.get('caption')
		image = request.FILES.getlist('postPhoto', False)
		audience = request.POST.get('post_audience')

		if not image and len(caption) == 0 or caption.isspace():
			messages.success(request, 'No contents added in the post.')
			return redirect('profile_app:profileTimeline', username = username)
		else:
			if audience == 'public':
				post = Post.objects.create(
						author = author,
						caption = caption,
						post_type = 'post',
						post_audience = 'public',
					)
			elif audience == 'followers':
				post = Post.objects.create(
						author = author,
						caption = caption,
						post_type = 'post',
						post_audience = 'followers',
					)
			elif audience == 'private':
				post = Post.objects.create(
						author = author,
						caption = caption,
						post_type = 'post',
						post_audience = 'private',
					)
			if image:
				for image in image:
					fs = FileSystemStorage()
					name = fs.save(image.name, image)
					url = fs.url(name)
					PostImage.objects.create(
							user = user,
							postid = post,
							image = url,
						)
		sendNotifiaction(request, post)
		followed_by = ProfileDetails.objects.filter(following = request.user)
		for followed_by in followed_by:
			Notifications.objects.create(
					post = post,
					sender = request.user,
					user = followed_by.user,
					notification_type = 1,
				)

	return redirect('profile_app:profileTimeline', username = username)

def editPost(request, id):
	post = Post.objects.get(id = id)
	if request.method == 'POST':
		image = request.FILES.getlist('postPhoto', False)
		post.caption = request.POST.get('caption')
		if image:
			for image in image:
				fs = FileSystemStorage()
				name = fs.save(image.name, image)
				url = fs.url(name)
				postImage.image = url
				postImage.save()
		post.save()

	return redirect('profile_app:profileTimeline', username = request.user)

def deletePost(request, id):
	post = Post.objects.get(id = id).delete()
	return redirect('profile_app:profileTimeline', username = request.user)

def viewPost(request, id):
	post = Post.objects.get(pk = id)
	my_profile = ProfileDetails.objects.get(user = request.user)
	try:
		notifications = Notifications.objects.filter(post = post.id).order_by('-date')
		for notifications in notifications:
			notifications.is_seen = 1
			notifications.save()
			print(notifications.is_seen)
	except:
		pass

	context = {
		'post': post,
		'my_profile': my_profile,
	}
	return render(request, 'Profile/Timeline/postDetails.html', context)


def like_unlike(request, id):
	post = Post.objects.get(pk = id)
	sender = User.objects.get(username = request.user)
	if sender in post.like.all():
		post.like.remove(sender)
		Notifications.objects.get(post = post).delete()
	else:
		post.like.add(sender)
		Notifications.objects.create(
				post = post,
				sender = sender,
				user = post.author.user,
				notification_type = 2,
			)
	return redirect('profile_app:profileTimeline', username = sender.username)

@login_required(login_url='UserAuthentication_app:login')
def comment(request, post, username):
	user = User.objects.get(username = username)
	post = Post.objects.get(pk = post)
	body = request.POST.get('comment')
	if request.method == 'POST':
		Comments.objects.create(
				user = user,
				post = post,
				body = body,
			)
		Notifications.objects.create(
				post = post,
				sender = request.user,
				user = post.author.user,
				notification_type = 3,
			)
	return redirect('profile_app:profileTimeline', username = username)

@login_required(login_url='UserAuthentication_app:login')
def replyComment(request, post, username, comment):
	user = User.objects.get(username = username)
	post = Post.objects.get(pk = post)
	comment = Comments.objects.get(pk = comment)
	body = request.POST.get('replyComment')
	if request.method == 'POST':
		ReplyComments.objects.create(
				comment = comment,
				user = user,
				post = post,
				body = body,
			)
	return redirect('profile_app:profileTimeline', username = username)
	
@login_required(login_url='UserAuthentication_app:login')
def notifications(request, username):
	unReadNotification = 0
	user = request.user
	notifications = Notifications.objects.filter(user = user).order_by('-date')
	for notification in notifications:
		if not notification.is_seen:
			unReadNotification = unReadNotification + 1
	context = {
		'notifications': notifications,
		'unReadNotification': unReadNotification,
	}
	return render(request, 'Profile/notifications.html', context)

@login_required(login_url='UserAuthentication_app:login')
def markAllNotificationRead(request):
	user = request.user
	notifications = Notifications.objects.filter(user = user).order_by('-date')
	for notifications in notifications:
		notifications.is_seen = 1
		notifications.save()
	context = {
		'notifications': notifications,
	}
	return redirect('profile_app:notifications', username = request.user)

@login_required(login_url='UserAuthentication_app:login')
def settings(request, username):
	context = {}
	return render(request, 'Profile/settings.html', context)



@login_required(login_url='UserAuthentication_app:login')
def updateProfilePic(request, username):
	user1 = User.objects.get(username = username)
	user = ProfileDetails.objects.select_related('user').get(user = user1.id)	
	if request.method == 'POST':
		caption = request.POST.get('profileCaption')
		image = request.FILES.get('profileImage', False)
		if not image:
			messages.success(request, 'No image selected')
			return redirect('profile_app:profileTimeline', username = username)
		else:
			fs = FileSystemStorage()
			name = fs.save(image.name, image)
			url = fs.url(name)
			user.profile_pic = url
			user.save()

			post = Post.objects.create(
					author = user,
					caption = caption,
					post_type = 'profile_picture',
					post_audience = 'public',
				)
			PostImage.objects.create(
					user = user1,
					postid = post,
					image = url,
				)

	return redirect('profile_app:profileTimeline', username = username)

@login_required(login_url='UserAuthentication_app:login')
def updateBio(request, username):
	user = User.objects.get(username = username)
	user = ProfileDetails.objects.select_related('user').get(user = user.id)
	if request.method == 'POST':
		bio = request.POST['bio']
		if len(bio) == 0 or bio.isspace():
			user.bio = None
		else:
			user.bio = bio
		user.save()
	return redirect('profile_app:profileTimeline', username = username)
