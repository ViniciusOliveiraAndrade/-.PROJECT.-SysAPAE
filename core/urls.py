from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('Registro/', views.registro, name='registro'),
    path('Ajuda', views.help, name='help'),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^registrar/$', views.registrar, name="registrar"),
]