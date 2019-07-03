from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
app_name = 'Chat_app'
from .views import IndexView
urlpatterns = [
    url(r'^$',IndexView.as_view(), name='home_page'),
]
