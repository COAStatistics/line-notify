from django.urls import path
from . import views

app_name = 'linenotify'

urlpatterns = [
    path('', views.home, name='home'),
    path('callback/', views.callback, name='callback'),
    path('push/', views.push, name='push'),
]
