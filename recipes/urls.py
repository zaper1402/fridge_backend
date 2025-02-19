from django.urls import path
from . import views

urlpatterns = [
    path('cuisines', views.get_cusines_tags),
    path('get-recipes', views.get_recipes_by_cuisine),
    path('get-matching-products', views.get_matching_product),
    path('favourite', views.recipe_favourite),
]