from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import datetime, timedelta
from user.models import Entry, WishlistProduct, Cuisine, Meals, FavRecipes
from core.serializers import RecipeDetailsSerializer, RecipesSerializer, HomeDataSerializer
from product.enums import *

# Create your views here.


@api_view(["GET"])
def get_food_data(request):
    return Response({
        "category": CATEGORIES,
        "quantity": QUANTITY_TYPES,
        "allergy": ALLERGY_TAGS
    }, status=200)


@api_view(['POST'])
def update_quantity(request):
    try:

        entries_data = request.data.get('entries', []) 
        if not entries_data:
            return Response(
                {"error": f"entry id is required"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        entries_to_update = []
    
        for entry_data in entries_data:
            entry_id = entry_data.get('entry_id')
            quantity = entry_data.get('quantity')

            if entry_id is None or quantity is None:
                continue  # Skip invalid entries

            entry = Entry.objects.filter(id=entry_id).first()
            if entry:
                entry.quantity = quantity
                entries_to_update.append(entry)
        print(entries_to_update)
        if entries_to_update:
            Entry.objects.bulk_update(entries_to_update, ['quantity'])  # Efficient batch update

        return Response(status=200) 
    except Exception as err:
        return Response(
            {"error":  {str(err)}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def expiry(request):
    try:
        user_id = request.GET.get('user_id', '')
        expiry_start = now()
        expiry_end = expiry_start + timedelta(days=10)

        entries = Entry.objects.filter(
            expiry_date__gte=expiry_start,
            expiry_date__lte=expiry_end,
            user_inventory__user_id=user_id
        ).values('expiry_date', 'user_inventory__product__name')
        return Response(list(entries), status=200) 
    except Exception as err:
        return Response(
            {"error":  {str(err)}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def home_data(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        serializer = HomeDataSerializer(data={'user_id': user_id})
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    else:
        return Response({"error": "Method not allowed."}, status=405)
    
@api_view(['POST'])
def add_wishlist(request):
    try:
        product_id = request.data.get('product_id', '')
        user_id = request.data.get('user_id', '')
        if not user_id and not product_id:
            return Response({"error": f"Product and user is important"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        WishlistProduct.objects.create(user_id=user_id, product_id=product_id)
        return Response({"message": "Product added to wishlist"}, status=200)
    except Exception as err:
        return Response(
            {"error": f"Error: {str(err)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def remove_wishlist(request):
    try:
        product_id = request.data.get('product_id', '')
        user_id = request.data.get('user_id', '')
        if not user_id and not product_id:
            return Response({"error": f"Product and user is important"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        WishlistProduct.objects.filter(user_id=user_id, product_id=product_id).delete()
        return Response({"message": "Product deleted from wishlist"}, status=200)
    except Exception as err:
        return Response(
            {"error": f"Error: {str(err)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def list_wishlist(request):
    try:
        user_id = request.GET.get('user_id', '')
        if not user_id:
            return Response({"error": f" user id is important"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        products = WishlistProduct.objects.filter(user_id=user_id).values('product__name', 'product_id')
        return Response({"data": list(products)}, status=200)
    except Exception as err:
        return Response(
            {"error": f"Error: {str(err)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_cuisine_list(request):
    data = Cuisine.objects.values('id', 'name', 'image_url')
    return Response({"data": list(data)}, status=200)



@api_view(['GET'])
def list_favs(request):
    request_data = request.GET
    user_id = request_data.get('user_id', '')
    items = FavRecipes.objects.filter(user_id=user_id).values_list('recipes_id', flat=True)
    meals = Meals.objects.filter(id__in=items)
    serializer = RecipesSerializer(meals, many=True, context={'favs':True})
    return Response({"data": serializer.data}, status=200)

@api_view(['POST'])
def add_favs(request):
    recipe_id = request.data.get('product_id', '')
    user_id = request.data.get('user_id', '')
    FavRecipes.objects.create(recipes_id=recipe_id, user_id=user_id)
    return Response({"message": "Recipe added to favorites"}, status=200)

@api_view(['POST'])
def remove_favs(request):
    recipe_id = request.data.get('product_id', '')
    user_id = request.data.get('user_id', '')
    FavRecipes.objects.filter(recipes_id=recipe_id, user_id=user_id).delete()
    return Response({"message": "Recipe added to favorites"}, status=200)



@api_view(['GET'])
def get_recipes(request):
    request_data = request.GET
    user_id = request_data.get('user_id', '')
    meal_type = request_data.get('type', '')
    cuisine = request_data.get('cuisine', '')
    if not (user_id or meal_type or  cuisine): 
        return Response({"error": f" user_id, meal_type, cuisine is important"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    favs = FavRecipes.objects.filter(user_id = user_id).values_list('recipes_id', flat=True)
    items = Meals.objects.filter(meal_type=meal_type, category_id=cuisine)
    serializer = RecipesSerializer(items, many=True, context={"fav_meals":favs})
    return Response({"data": serializer.data}, status=200)


    
@api_view(['GET'])
def get_recipe_details(request):
    request_data = request.GET
    recipe_id = request_data.get('id', '')
    items = Meals.objects.filter(id=recipe_id).first()
    serializer = RecipeDetailsSerializer(items)
    return Response({"data": serializer.data}, status=200)


@api_view(['POST'])
def lets_cook(request):
    return Response({"data": "cooked"}, status=200)


