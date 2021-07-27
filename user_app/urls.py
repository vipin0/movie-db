from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import ObtainAuthToken
from user_app import views

urlpatterns = [
    path('login/',ObtainAuthToken.as_view(),name='login'),
    path('register/',views.RegisterUser.as_view(),name='register'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
]
