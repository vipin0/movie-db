from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

class RegisterSerializer(ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    password = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['username','email','password','password2']
        extra_kwargs={
            'password':{'write_only':True,}
        }
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        email = self.validated_data['email']
        username = self.validated_data['username']

        if User.objects.filter(email=email).exists():
            raise ValidationError({"error":"Email already exists!"},code=400)
            
        if password!=password2:
            raise ValidationError({"error":"Password1 and password2 must be same!"},code=400)
        user = User(username=username,email=email)
        user.set_password(password)
        user.save()
        return user
