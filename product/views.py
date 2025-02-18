from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product
from product.serializers import ProductSerializer


@csrf_exempt
@api_view(['GET'])
def get_all_categories(request):
    categories = Product.objects.values('category').distinct()
    return Response(categories, status=200)


@csrf_exempt
@api_view(['GET'])
def get_product_list(request):
    # if(request.method == 'GET'):    
        # token = request.headers.get('Authorization')
        # verified_token = verify_token_direct(token)
        # if verified_token.status_code != 200:
        #     return verified_token
        # else:   
    filters = {}
    search_string = request.GET.get('search', '')
    if search_string:            
        filters['name__icontains'] = search_string
    products = Product.objects.filter(**filters).values('name', 'id','standard_expiry_days')
    return Response({'products':products}, status=201) 
    # else:
    #     return Response({"error": "Method not allowed."}, status=405)