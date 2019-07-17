"""Farazan_Parvari_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
import Farzand_Parvari_app.urls as urls_App
#import Chat_app.urls as chat_url
from django.conf.urls import include
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'chat/', include(chat_url)),
    url(r'', include(urls_App)),
]
admin.site.site_header = "Farzand Parvari Admin"
admin.site.site_title = "Farzand Parvari Admin Portal"
admin.site.index_title = "Welcome to Farzand Parvari Researcher Portal"
handler404 = 'Farzand_Parvari_app.views.handler404'
handler500 = 'Farzand_Parvari_app.views.handler500'
