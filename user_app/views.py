from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
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

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"message":"Logout successful!"},status=status.HTTP_200_OK)


