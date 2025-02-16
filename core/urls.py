from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home_data, name='update_user'),
    path('dropdown-data', views.get_food_data, name='dropdownData'),
    path('update-quantity', views.update_quantity, name='update_quantity'),
    path('expiry', views.expiry, name='expiry'),
    path('add-product-wishlist', views.add_wishlist, name='add_wishlist'),
    path('remove-product-wishlist', views.remove_wishlist, name='remove_wishlist'),
    path('list-product-wishlist', views.list_wishlist, name='list_wishlist'),
    path('list-cuisine-wishlist', views.get_cuisine_list, name='get_cuisine_list'),
    
    path('list-recipes', views.get_recipes, name='get_recipes'),
    path('detail-recipes', views.get_recipe_details, name='get_cuisine_list'),
    path('lets-cook', views.lets_cook, name='lets_cook'),
    path('add-favs', views.add_favs, name='add_favs'),
    path('remove-favs', views.remove_favs, name='remove_favs'),
    path('list-favs', views.list_favs, name='list_favs'),
    

    
]