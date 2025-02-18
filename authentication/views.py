from rest_framework.response import Response
from django.contrib.auth.hashers import check_password, make_password
from firebase_admin import auth as firebase_auth
from rest_framework.decorators import api_view
from rest_framework import status
from user.models import User
from user.serializers import UserSerializer
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def login(request):
    try:
        # print(User.objects.filter(email='ashirkul@gmail.com').values('email', 'password'))
        email = request.data.get('email')
        password = request.data.get('password')
        usr = User.objects.filter(email=email).first()
        print(password, usr.password)
        if check_password(password, usr.password):
            token, api_key = Token.objects.get_or_create(user_id=usr.id)
            serialized_user = UserSerializer(usr)
            serialized_data = serialized_user.data
            serialized_data['api_key'] = api_key
            serialized_data['token'] = token.key
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            raise PasswordError(AFM0014)
    except Exception as err:
        return Response(
            {"error": f"User verification failed: {str(err)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@api_view(['POST'])
def verify_token(request):
    token = request.data.get('token')
    resp = verify_token_direct(token)
    if resp.status_code == 200:
        uid = resp.data.get('uid')
        email = firebase_auth.get_user(uid).email
        if email is None or email == "" or User.objects.filter(email=email).exists() is False:
            photo = firebase_auth.get_user(uid).photo_url
            phone_number = firebase_auth.get_user(uid).phone_number
            display_name = firebase_auth.get_user(uid).display_name
            temp_user = User(name=display_name, email=email, photo=photo, phone_number=phone_number)
            serialized_user = UserSerializer(temp_user)
            serialized_user.data['new_user'] = True
            return Response(serialized_user.data, status=status.HTTP_200_OK)
        else:
            user = User.objects.get(email=email)
            serialized_user = UserSerializer(user)
            serialized_user.data['new_user'] = False
            return Response(serialized_user.data, status=status.HTTP_200_OK)
    else:
        return resp
   
    
def verify_token_direct(token):
    if not token:
        return Response(
            {"error": "No token provided."},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token['uid']

        return Response(
            {"message": "Token is valid.", "uid": uid},
            status=status.HTTP_200_OK
        )

    except firebase_auth.InvalidIdTokenError:
        return Response(
            {"error": "Invalid token."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except firebase_auth.ExpiredIdTokenError:
        return Response(
            {"error": "Token has expired."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        return Response(
            {"error": f"Token verification failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )