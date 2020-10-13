from django.apps import AppConfig


class UserauthenticationConfig(AppConfig):
    name = 'UserAuthentication'

    def ready(self):
    	import UserAuthentication.signals
