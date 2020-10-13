from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'UserAuthentication_app'
urlpatterns = [
		path('activate/<uidb64>/<token>', views.activateAccount, name = "activateAccount"),
		path('sendmail/<user>', views.sendMail, name = "sendMail"),

		path('login', views.loginPage, name = "login"),
		path('register', views.registerPage, name = "register"),
		path('logout', views.logOutUSer, name = "logout"),

		path('resetPassword', auth_views.PasswordResetView.as_view(template_name = "UserAuthentication/resetPassword.html"), name = "password_reset"),

]