from rest_framework.parsers import JSONParser
from authentication.views import verify_token_direct
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

#TODO
@api_view(['POST'])
def cuisine_type(request):

    #have the options for the cuisine types 
    return Response()

def meal_selection(request, meal_type):

    #get inventory and filer recipies based on cusine type and what is available in inventory

    #get list of the top 10 recipies, including name and image for display and ID  
    return Response()

def meal_recipe(request):
    return