from django.urls import path
from . import views

urlpatterns = [
    #get user with uid request param
    path('get', views.get_user, name='get_user'),
    path('update', views.update_user, name='update_user'),
    path('addProduct', views.addUserProduct, name='addUserProduct'),
    path('get-all-categories', views.getUserProductCategories, name='get_all_categories'),
    path('get-products', views.getUserProductsByCategory, name='get_user_products'),    
    path('update-products', views.updateUserProducts, name='update_user_products'),
]