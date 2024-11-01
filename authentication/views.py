from django.http import JsonResponse
from firebase_admin import auth
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def verify_token(request):
    token = request.data.get('token')

    if not token:
        return JsonResponse(
            {"error": "No token provided."},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

        return JsonResponse(
            {"message": "Token is valid.", "uid": uid},
            status=status.HTTP_200_OK
        )

    except auth.InvalidIdTokenError:
        return JsonResponse(
            {"error": "Invalid token."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except auth.ExpiredIdTokenError:
        return JsonResponse(
            {"error": "Token has expired."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Token verification failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
