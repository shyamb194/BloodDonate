from django.urls import path
from . import views

app_name = 'profile_app'
urlpatterns = [
	path('followUnfollow/<username>', views.follow_unfollow, name = "followUnfollow"),
	path('<username>/', views.profileTimeline, name = "profileTimeline"),
	path('createPost/<username>', views.createPost, name = "createPost"),
	path('updateProfilePic/<username>', views.updateProfilePic, name = "updateProfilePic"),
	path('updateProfile/<username>', views.updateProfile, name = "updateProfile"),
	path('updateBio/<username>', views.updateBio, name = "updateBio"),
	path('<username>/notifications', views.notifications, name = "notifications"),
	path('<username>/settings', views.settings, name = "settings"),
	path('<username>/following', views.profileTimeline, name = "following"),
	path('<username>/photos', views.profileTimeline, name = "photos"),
	path('<username>/about', views.profileTimeline, name = "about"),
]