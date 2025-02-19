from rest_framework.parsers import JSONParser
from .serializers import UserSerializer, AddProductFormSerializer
from django.http import HttpResponse
from authentication.views import verify_token_direct
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User, UserProduct
from user.serializers import UserProductSerializer, NotifSerializer
from product.models import Product
from datetime import datetime, timedelta

@csrf_exempt
@api_view(['GET'])
def get_user(request):
    if(request.method == 'GET'):    
        token = request.headers.get('Authorization')
        verified_token = verify_token_direct(token)
        if verified_token.status_code != 200:
            # return get user from jwt token
            uid = request.GET.get('uid')
            user = User.objects.get(id=uid)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        else:
            user = getUserFromToken(verified_token)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
    else:
        return Response({"error": "Method not allowed."}, status=405)

@csrf_exempt
@api_view(['POST'])
def update_user(request):
    if(request.method == 'POST'):    
        # token = request.headers.get('Authorization')
        # verified_token = verify_token_direct(token)
        # if verified_token.status_code != 200:
        #     return verified_token
        # else:
            data = request.data
            email = data.get('email')
            data['username'] = email
            if email is None or email == "":
                return Response({"error": "Email is required."}, status=400)
            elif User.objects.filter(email=email).exists() is False:
                serializer = UserSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                else:
                    return Response(serializer.errors, status=400)
            else:
                user = User.objects.get(email=email)
                serializer = UserSerializer(user, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                else:
                    return Response(serializer.errors, status=400)
    else:
        return Response({"error": "Method not allowed."}, status=405)
    

def getUserFromToken(verified_token):
    return User.objects.get(email=verified_token.data['email'])
    

@csrf_exempt
@api_view(['POST'])
def addUserProduct(request):
    if(request.method == 'POST'):    
        # token = request.headers.get('Authorization')
        # verified_token = verify_token_direct(token)
        # if verified_token.status_code != 200:
        #     return verified_token
        # else:   
            data = request.data
            # user = getUserFromToken(verified_token)
            date =  datetime.strptime(data['expiry'], '%d/%m/%Y').date()
            data['expiry'] = date.strftime('%Y-%m-%d')
            print(data)
            serializer = AddProductFormSerializer(data=data)
            if serializer.is_valid():
                product = serializer.save()
                return Response(product, status=201) 
                
            else:
                return Response(serializer.errors, status=400)
    else:
        return Response({"error": "Method not allowed."}, status=405)

#def get user product categories
@csrf_exempt
@api_view(['GET'])
def getUserProductCategories(request):
    if(request.method == 'GET'):    
        # token = request.headers.get('Authorization')
        # verified_token = verify_token_direct(token)
        # if verified_token.status_code != 200:
        #     return verified_token
        # else:   
        # user = getUserFromToken(verified_token)
        user_id = request.GET.get('user_id')
        user_products = UserProduct.objects.filter(user_id=user_id).values('product__category').distinct()
        product_categories = [{'product_category': x['product__category']} for x in user_products]
        return Response({'categories':product_categories}, status=200)
    else:
        return Response({"error": "Method not allowed."}, status=405)
    
#def get user products by category
@csrf_exempt
@api_view(['GET'])
def getUserProductsByCategory(request):
    if(request.method == 'GET'):    
        # token = request.headers.get('Authorization')
        # verified_token = verify_token_direct(token)
        # if verified_token.status_code != 200:
        #     return verified_token
        # else:   
        # user = getUserFromToken(verified_token)
        user_id = request.GET.get('user_id')
        category = request.GET.get('category')
        user_products = UserProduct.objects.filter(user_id=user_id, product__category=category)
        serializer = UserProductSerializer(user_products, many=True)
        return Response({"inventory":serializer.data}, status=200)
    else:
        return Response({"error": "Method not allowed."}, status=405)


# update user products from user products list
@csrf_exempt
@api_view(['POST'])
def updateUserProducts(request):
    if(request.method == 'POST'):    
        # token = request.headers.get('Authorization')
        # verified_token = verify_token_direct(token)
        # if verified_token.status_code != 200:
        #     return verified_token
        # else:   
        # user = getUserFromToken(verified_token)
        data = request.data
        user = User.objects.get(id=data['user_id'])
        if not user:
            return Response({"error": "User not found."}, status=404)
        user_products = data['user_products']
        for user_product_data in user_products:
            product_id = user_product_data['id']
            print(product_id)
            if not UserProduct.objects.filter(id=product_id).exists():
                return Response({"error": "Product not found."}, status=404)
            user_product = UserProduct.objects.get(id=product_id)
            print(f'{product_id}, {user_product_data["quantity"]}') 
            user_product_serialized = UserProductSerializer(user_product, data={
                'quantity': user_product_data['quantity'],
                'quantity_type': user_product_data['quantity_type']
            },partial=True)
            if user_product_serialized.is_valid():
                user_product_serialized.save()
            else:
                return Response(user_product_serialized.errors, status=400)
        return Response({"message": "Products updated successfully."}, status=200)
    else:
        return Response({"error": "Method not allowed."}, status=405)


# def products within 10 days
@csrf_exempt
@api_view(['GET'])
def getNotifications(request):
    if(request.method == 'GET'):    
        # token = request.headers.get('Authorization')
        # verified_token = verify_token_direct(token)
        # if verified_token.status_code != 200:
        #     return verified_token
        # else:   
        # user = getUserFromToken(verified_token)
        user_id = request.GET.get('uid')
        user = User.objects.get(id=user_id)
        if not user:
            return Response({"error": "User not found."}, status=404)
    
        user_products = UserProduct.objects.filter(user=user, expiry_date__lte=datetime.now() + timedelta(days=10)).order_by('expiry_date')
        sorted_products = sorted(user_products, key=lambda x: x.expiry_date)
        serializer = NotifSerializer(sorted_products, many=True)
        return Response({"notifs":serializer.data}, status=200)
    else:
        return Response({"error": "Method not allowed."}, status=405)