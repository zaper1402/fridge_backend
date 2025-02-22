from .models import Recipe
from rest_framework import serializers
from .enums import Cuisine

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class CuisineSerializer(serializers.Serializer):
    cuisines = serializers.SerializerMethodField()

    def get_cuisines(self, obj):
        cuisines = []
        cuisines = Cuisine.names
        distinct_cuisines = list(set(cuisines))
        return distinct_cuisines
    
