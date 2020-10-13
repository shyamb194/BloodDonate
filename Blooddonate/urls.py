"""Blooddonate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('', include('Profile.urls')),
    path('', include('UserAuthentication.urls')),

    path('resetPasswordConfirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "UserAuthentication/passwordResetConfirm.html"), name = "password_reset_confirm"),
    path('resetPasswordSent', auth_views.PasswordResetDoneView.as_view(template_name = "UserAuthentication/resetPasswordSent.html"), name = "password_reset_done"),
    path('resetPasswordComplete', auth_views.PasswordResetCompleteView.as_view(template_name = "UserAuthentication/passwordResetComplete.html"), name = "password_reset_complete"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
