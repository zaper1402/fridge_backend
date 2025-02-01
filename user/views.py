from rest_framework.parsers import JSONParser
from .serializers import UserSerializer, AddProductFormSerializer
from django.http import HttpResponse
from authentication.views import verify_token_direct
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User, UserProduct
from user.serializers import UserProductSerializer
from product.models import Product


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
                    return Response(serializer.data, status=201)
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
            # data['user_id'] = 2
            serializer = AddProductFormSerializer(data=data)
            if serializer.is_valid():
                product = serializer.save()
                return Response(product, status=201) 
                
            else:
                return Response(serializer.errors, status=400)
    else:
        return Response({"error": "Method not allowed."}, status=405)

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
    products = Product.objects.filter(**filters).values('name', 'id')
    return Response(list(products), status=201) 
    # else:
    #     return Response({"error": "Method not allowed."}, status=405)
