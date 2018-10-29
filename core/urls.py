from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    url(r'^login/$', login, {'template_name': 'core/login.html'}, name="login"),
    url(r'^logout/$', logout, {'template_name': 'core/logout.html'}, name="logout"),
    url(r'^registrar/$', views.registrar, name="registrar"),

    

]