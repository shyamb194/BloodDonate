from django.urls import path
from . import views

app_name = 'profile_app'
urlpatterns = [
	path('<username>/', views.profileTimeline, name = "profileTimeline"),
	path('followUnfollow/<username>', views.follow_unfollow, name = "followUnfollow"),
	path('updateProfilePic/<username>', views.updateProfilePic, name = "updateProfilePic"),
	path('updateBio/<username>', views.updateBio, name = "updateBio"),
	path('updateProfile/<username>', views.updateProfile, name = "updateProfile"),

	path('createPost/<username>', views.createPost, name = "createPost"),
	path('viewPost/<id>', views.viewPost, name = "viewPost"),
	path('editPost/<id>', views.editPost, name = "editPost"),	
	path('deletePost/<id>', views.deletePost, name = "deletePost"),
	path('like_unlike/<id>', views.like_unlike, name = "likeUnlike"),
	path('comment/<post>/<username>', views.comment, name = "comment"),
	path('comment/<post>/<username>/<comment>', views.replyComment, name = "replyComment"),
	
	path('<username>/following', views.profileTimeline, name = "following"),
	path('<username>/photos', views.profileTimeline, name = "photos"),
	path('<username>/about', views.profileTimeline, name = "about"),

	path('<username>/notifications', views.notifications, name = "notifications"),
	path('markAllNotificationRead', views.markAllNotificationRead, name = "markAllNotificationRead"),
	path('<username>/settings', views.settings, name = "settings"),
]