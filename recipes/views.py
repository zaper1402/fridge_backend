from django.shortcuts import render
from .models import Recipe , Favourite
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializers import RecipeSerializer
from user.models import UserProduct
from user.views import verify_token_direct, getUserFromToken
from user.serializers import UserProductSerializer
from django.db.models import Q
from .serializers import CuisineSerializer

# Create your views here.


@csrf_exempt
@api_view(['GET'])
def get_cusines_tags(request):
    try:
        cuisines = CuisineSerializer(request.data).data['cuisines']
        return Response({"cuisines": cuisines}, status=200)
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


@csrf_exempt
@api_view(['GET'])
def get_matching_product(request):
    if(request.method == 'GET'):    
        # token = request.headers.get('Authorization')
        # verified_token = verify_token_direct(token)
        # if verified_token.status_code != 200:
        #     return verified_token
        # else:   
        # user = getUserFromToken(verified_token)
        recipe_id = request.GET.get('recipe_id')
        if not recipe_id:
            return Response({"error": "Recipe ID is required."}, status=400)
        user_id = request.GET.get('uid')
        if not user_id:
            return Response({"error": "User ID is required."}, status=400)
       
        recipe = Recipe.objects.get(id=recipe_id)
        if not recipe:
            return Response({"error": "Recipe not found."}, status=404)
        ingredients = recipe.ingredients
        ingredients.append("juice mango ultimate")
        print(ingredients)
        query = Q()
        for ingredient in ingredients:
            for word in ingredient.split():
                query |= Q(product__name__icontains=word)
        
        products = UserProduct.objects.filter(query, user_id=user_id)       
        serializer = UserProductSerializer(products, many=True)
        return Response({"products":serializer.data}, status=200)
    else:
        return Response({"error": "Method not allowed."}, status=405)
    

@csrf_exempt
@api_view(['GET', 'POST'])
def recipe_favourite(request):
    if request.method == 'GET':
        user_id = request.GET.get('uid')
        if not user_id:
            return Response({"error": "User ID is required."}, status=400)
        favourites = Favourite.objects.filter(user_id=user_id)
        recipes = Recipe.objects.filter(id__in=[f.recipe_id for f in favourites])
        serializer = RecipeSerializer(recipes, many=True)
        return Response({"recipes": serializer.data}, status=200)
    elif request.method == 'POST':
        data = request.data
        user_id = data.get('uid')
        recipe_id = data.get('recipe_id')
        favourite = data.get('favourite')
        if not user_id:
            return Response({"error": "User ID is required."}, status=400)
        if not recipe_id:
            return Response({"error": "Recipe ID is required."}, status=400)
        if favourite is None or not isinstance(favourite, bool):
            return Response({"error": "Favourite status is required."}, status=400)
        
        if favourite:
            Favourite.objects.create(user_id=user_id, recipe_id=recipe_id)
        else:
            Favourite.objects.filter(user_id=user_id, recipe_id=recipe_id).delete()
        favourites = Favourite.objects.filter(user_id=user_id)
        recipes = Recipe.objects.filter(id__in=[f.recipe_id for f in favourites])
        serializer = RecipeSerializer(recipes, many=True)
        return Response({"recipes": serializer.data}, status=200)
    else:
        return Response({"error": "Method not allowed."}, status=405)
