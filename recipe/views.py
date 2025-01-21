from rest_framework.parsers import JSONParser
from authentication.views import verify_token_direct
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

#TODO
@api_view(['POST'])
def meal_type(request):
    return Response()

def meal_selection(request, meal_type):
    return Response()