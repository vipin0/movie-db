from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from user_app.serializers import RegisterSerializer
# Create your views here.
from user_app import models

@api_view(['POST'])
def regiser_user(request):

    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {}
            data['username'] = user.username
            data['email'] = user.email
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class RegisterUser(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request,*args, **kwargs):
        response = super(RegisterUser, self).create(request, *args, **kwargs)
        username=response.data['username']
        user = User.objects.get(username=username)
        token, created = Token.objects.get_or_create(user=user)
        response.status = status.HTTP_200_OK
        response.data['token'] = token.key
        return response

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"message":"Logout successful!"},status=status.HTTP_200_OK)


