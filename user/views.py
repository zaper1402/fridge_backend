from rest_framework.parsers import JSONParser
from .serializers import UserSerializer
from django.http import HttpResponse
from authentication.views import verify_token_direct
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User


@csrf_exempt
@api_view(['POST'])
def update_user(request):
    if(request.method == 'POST'):    
        token = request.headers.get('Authorization')
        verified_token = verify_token_direct(token)
        if verified_token.status_code != 200:
            return verified_token
        else:
            data = request.data
            email = data.get('email')
            if email is None or email == "" or User.objects.filter(email=email).exists() is False:
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
        return HttpResponse({"error": "Method not allowed."}, status=405)
