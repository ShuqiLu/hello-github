"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
'''
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
'''
import django
from django.conf.urls import url
from . import view,search,search2,settings
urlpatterns = [
    url(r'^hello$', view.hello),
    url(r'^search-form$', search.search_form),
    #url(r'^search-form2$', search.search_form),
    #url(r'^search$', search.search),
    #url(r'^search$', search.search_form),
    url(r'^search-post$', search2.search_post),
    url(r'^getpath$', search2.getpath),
    url(r'^getpathten$', search2.getpathten),
    url(r'^getnews$', search2.getnews),
    url(r'^static/(?P<path>.*)$', django.views.static.serve,{ 'document_root': settings.STATIC_URL })
]