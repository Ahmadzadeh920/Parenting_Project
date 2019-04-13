from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from .views import index


urlpatterns = [
    url(r'^$', index, name='homepage'),  # The start point for index view
    url(r'^accounts/login/$', login, name='login'),  # The base django login view
    url(r'^accounts/logout/$', logout, name='logout'),  # The base django logout view
    url(r'^admin/', admin.site.urls),  # etc :D
]
