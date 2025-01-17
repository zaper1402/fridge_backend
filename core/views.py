from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import HomeDataSerializer
from rest_framework.response import Response
from django.utils.timezone import now

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
    

