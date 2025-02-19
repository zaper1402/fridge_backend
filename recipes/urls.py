from django.urls import path
from . import views

urlpatterns = [
    path('cuisines', views.get_cusines_tags),
    path('get-recipes', views.get_recipes_by_cuisine),
]