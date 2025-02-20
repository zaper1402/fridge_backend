from django.shortcuts import render
from user.models import UserProduct, Entry, Meals
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import HomeDataSerializer
from rest_framework.response import Response
from django.utils.timezone import now
from product.models import Product
from datetime import datetime, timedelta
from user.models import Entry, WishlistProduct, Cuisine, Meals, FavRecipes
from core.serializers import RecipeDetailsSerializer, RecipesSerializer, HomeDataSerializer
from product.enums import *

# Create your views here.

@api_view(['POST'])
def home_data(request):
    if request.method == 'POST':
        serializer = HomeDataSerializer(data={'user_id': 2})
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

@api_view(['GET'])
def get_ingredients(request):
    request_data = request.GET
    recipe_id = request_data.get('id', '')
    user_id = request_data.get('user_id', '')
    items = Meals.objects.filter(id=recipe_id).first()
    ingredients = items.ingredients or []
    product_ids = [item.get('id', '') for item in ingredients]
    user_prod = UserProduct.objects.filter(product_id__in=product_ids, user_id=user_id).values_list('id', flat=True)
    from django.db.models import F  
    from django.utils.timezone import now

    entries = Entry.objects.filter(
        user_inventory__in=user_prod, quantity__gt=0, expiry_date__gt=now()
    ).annotate(
        product_name=F('user_inventory__product__name'),
        product_id=F('user_inventory__product_id')
    ).values('product_name', 'product_id', 'quantity')

    return Response({"data": entries}, status=200)


@api_view(['POST'])
def lets_cook(request):
    request_data = request.data
    user_id = request_data.get('user_id', '')
    ingredients = request_data.get('products', [])
    product_ids = [item.get('id', '') for item in ingredients]
    ingredients_dict ={item.get('id', ''):item.get('qt', '') for item in ingredients}
    user_prod = UserProduct.objects.filter(product_id__in=product_ids, user_id=user_id).values_list('id', flat=True)
    entries = Entry.objects.filter(
        user_inventory__in=user_prod, quantity__gt=0, expiry_date__gt=now()).order_by('-expiry_date')

    entries_dict ={}
    for item in entries:
        if item.user_inventory and item.user_inventory.product:
            if item.user_inventory.product.id in entries_dict:
                entries_dict[item.user_inventory.product.id]['quantity'] += item.quantity
            else:
                entries_dict[item.user_inventory.product.id] = {'quantity': item.quantity}
    
    uncooked_element = []
    for item in ingredients:
        product_id = item.get('id', '')
        if product_id in entries_dict.keys():
            existing_element = entries_dict.get(product_id, {})
            if existing_element.get('quantity', 0) <= item.get('qt', 0):
                uncooked_element.append(product_id)
    
    if uncooked_element:
        data = Product.objects.filter(id__in=uncooked_element).values_list('name', flat=True)
        return Response({"data": {"uncooked_element":data},}, status=200)    
    
    for item in ingredients:
        product_id = item.get("id", '')
        required_quantity = item.get("qt", '')
        entries = Entry.objects.filter(
            user_inventory__product_id=product_id, quantity__gt=0, expiry_date__gt=now()
        ).order_by('expiry_date')
        for entry in entries:
            if required_quantity <= 0:
                break  # Stop if fulfilled

            if entry.quantity <= required_quantity:
                # Deduct full stock from this entry
                required_quantity -= entry.quantity
                entry.quantity = 0  # Mark for deletion
            else:
                # Partial deduction
                entry.quantity -= required_quantity
                required_quantity = 0  # Fulfilled

            entry.save()  # Save the updated entry


    
    return Response({"data": "cooked"}, status=200)


