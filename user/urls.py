from django.urls import path
from . import views

urlpatterns = [
    path('update', views.update_user, name='update_user'),
    path('addProduct', views.addUserProduct, name='addUserProduct'),
    path('get-product-list', views.get_product_list, name='get_product_list'),
    
]