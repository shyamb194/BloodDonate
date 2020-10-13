from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import ProfileDetails
from django.contrib import messages

class MobileEmailUserAuthenticate(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email = username)
            if user.check_password(password):
                return user
        except:
            try:
                user = ProfileDetails.objects.select_related('user').get(contact = username)
                if user.user.check_password(password):
                    return user.user                    
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None