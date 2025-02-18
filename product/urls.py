from django.urls import path
from . import views

urlpatterns = [
    #get user with uid request param
    path('get-product-list', views.get_product_list, name='get_product_list')
]