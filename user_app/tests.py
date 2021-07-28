from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
# Create your tests here.

class RegisterTestCase(APITestCase):
    
    def test_register(self):
        data = {
                "username":"test",
                "email":"test@test.com",
                "password":"Password@123",
                "password2":"Password@123"
            } 
        response = self.client.post(reverse('register'),data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'],"test")
        self.assertEqual(response.data['email'],"test@test.com")

class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test",password="Test@1234")
    
    def test_login(self):
        data = {
            "username":"test",
            "password":"Test@1234"
        }
        response = self.client.post(reverse('login'),data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
