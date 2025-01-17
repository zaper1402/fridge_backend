from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home_data, name='update_user'),
]