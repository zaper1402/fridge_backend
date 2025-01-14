from django.urls import path
from . import views

urlpatterns = [
    path('update', views.update_user, name='update_user'),
    path('addProduct', views.addUserProduct, name='addUserProduct'),
]