from django.urls import path
from . import views

urlpatterns = [
    path('cuisine_type', views.meal_type, name='meal_type'),
    path('meal_selection', views.meal_selection, name='meal_selection'), #TODO
]