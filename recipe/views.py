from rest_framework.parsers import JSONParser
#from .serializers import UserSerializer
from django.http import HttpResponse
from authentication.views import verify_token_direct
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User