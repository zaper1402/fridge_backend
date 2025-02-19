from django.shortcuts import render
from .models import Recipe 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializers import RecipeSerializer

# Create your views here.


@csrf_exempt
@api_view(['GET'])
def get_cusines_tags(request):
    try:
        cuisines = Recipe.objects.values_list('cuisine_tags', flat=True)
        flat_cuisines = [item for sublist in cuisines for item in sublist]
        distinct_cuisines = list(set(flat_cuisines))
        return Response({"cusines":distinct_cuisines}, status=200)
    except Exception as e:
        return Response({"error":str(e)}, status=500)



@csrf_exempt
@api_view(['GET'])
def get_recipes_by_cuisine(request):
    cuisine = request.GET.get('cuisine')
    if not cuisine:
        return Response({"error":"Cuisine is required"}, status=400)
    try:
        recipes_data = Recipe.objects.filter(cuisine_tags__icontains=cuisine)
        recipes = RecipeSerializer(recipes_data, many=True).data
        limit = int(request.GET.get('limit', 20))
        breakfast = [recipe for recipe in recipes if any('BREAKFAST' in tag.upper() for tag in recipe['cuisine_tags'])][:limit]
        lunch = [recipe for recipe in recipes if any('LUNCH' in tag.upper() for tag in recipe['cuisine_tags'])][:limit]
        dinner = [recipe for recipe in recipes if any('DINNER' in tag.upper() for tag in recipe['cuisine_tags'])][:limit]
        
        separated_recipes = {
            "breakfast_recipes": breakfast,
            "lunch_recipes": lunch,
            "dinner_recipes": dinner
        }
    
        return Response(separated_recipes, status=200)
    except Exception as e:
        return Response({"error":str(e)}, status=500)

