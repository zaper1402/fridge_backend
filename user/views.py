from rest_framework.parsers import JSONParser
from .serializers import UserSerializer
from django.http import HttpResponse
from authentication.views import verify_token_direct
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_user(request):
    if(request.method == 'POST'):    
        data = JSONParser().parse(request)
        # token = request.headers.get('Authorization')

        # if not token:
        #     return HttpResponse({"error": "No token provided."}, status=400)

        # response = verify_token_direct(token)

        # if response.status_code != 200:
        #     return response

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse({serializer.data}, status=201)
        else:
            return HttpResponse(serializer.errors, status=400)
    else:
        return HttpResponse({"error": "Method not allowed."}, status=405)
