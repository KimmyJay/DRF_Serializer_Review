from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password

from user.models import User, UserType
from user.serializers import UserSerializer


# Create your views here.
class LoginLogout(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({'message': 'Login failed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        login(request, user)
        return Response({'message': 'Login succeeded.'}, status=status.HTTP_200_OK)

    def delete(self, request):
        logout(request)
        return Response({'message': 'Logout succeeded.'}, status=status.HTTP_200_OK)

class UserView(APIView):
    # get logged-in user info
    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user, context={"request": request})
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    # create a new user
    def post(self, request):
        user_type = request.data.get("usertype", '')
        password = request.data.get("password", '')
        context = {
            "request": request,
            "user_type": user_type,
            "password": password
        }

        user_serializer = UserSerializer(data=request.data, context=context)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    # edit logged-in user info
    def put(self, request):
        user = request.user
        user_type = request.data.get("usertype", '')
        password = request.data.get("password", '')
        context = {
            "request": request,
            "user_type": user_type,
            "password": password
        }

        user_serializer = UserSerializer(user, data=request.data, partial=True, context=context)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)



