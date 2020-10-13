from django.urls import path
from . import views

app_name = 'home_app'
urlpatterns = [
    path('', views.home, name = "home"),
    path('whoCandonateBlood', views.whoCandonateBlood, name = "whoCandonateBlood"),
    path('newsFeed', views.newsFeed, name = "newsFeed"),
    path('newsAndEvents', views.newsAndEvents, name = "newsAndEvents"),
]