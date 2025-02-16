from django.urls import path
from . import views

urlpatterns = [
    path('register-user', views.register_user, name='register_user'),
    path('profile', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('verify', views.verify_token, name='verify_token'),
]
