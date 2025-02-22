from .models import Recipe
from rest_framework import serializers
from .enums import Cuisine
from user.models import UserProduct
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

        
class RecipeCategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_id = self.context.get('user_id')
        self._limit = self.context.get('limit', 20)
        if self._user_id:
            self.user_products = UserProduct.objects.filter(user_id=self._user_id)
            self.user_product_ids = set(product.product_id for product in self.user_products)
            print(self.user_product_ids)

        
    breakfast_recipes = serializers.SerializerMethodField()
    lunch_recipes = serializers.SerializerMethodField()
    dinner_recipes = serializers.SerializerMethodField()


    class Meta:
        model = Recipe
        fields = ['breakfast_recipes', 'lunch_recipes', 'dinner_recipes']

    def get_breakfast_recipes(self, obj : QuerySet):
        recipes = obj.filter(cuisine_tags__icontains='BREAKFAST')
        return self.sort_by_matching_ingredients(recipes[:self._limit])
    
    def get_lunch_recipes(self, obj : QuerySet):
        recipes = obj.filter(cuisine_tags__icontains='LUNCH')
        return self.sort_by_matching_ingredients(recipes[:self._limit])
    
    def get_dinner_recipes(self, obj : QuerySet):
        recipes = obj.filter(cuisine_tags__icontains='DINNER')
        return self.sort_by_matching_ingredients(recipes[:self._limit])
    
    def sort_by_matching_ingredients(self, recipes):
        """
        Sort recipes by number of matching ingredients with user's products.
        Returns sorted recipes list with matching count.
        """
        # Convert QuerySet to list if needed
        recipes_list = list(recipes)

        def get_matching_count(recipe):
            recipe_ingredients = set(ingredient['id'] for ingredient in recipe.ingredients)
            return len(recipe_ingredients.intersection(self.user_product_ids))
        
        # Sort the list of recipes
        sorted_recipes = sorted(recipes_list, key=get_matching_count, reverse=True)
        
        # Create list of recipes with their matching counts
        recipes_with_matches = [
            {
                'recipe': RecipeSerializer(recipe).data,
                'matching_ingredients': get_matching_count(recipe),
                'total_ingredients': len(recipe.ingredients)
            }
            for recipe in sorted_recipes
        ]
        
        return recipes_with_matches

class CuisineSerializer(serializers.Serializer):
    cuisines = serializers.SerializerMethodField()

    def get_cuisines(self, obj):
        cuisines = []
        for Cu in Cuisine:
            cuisines.append({
                "id": Cu.name,
                "name": Cu.value
            })
        return cuisines

