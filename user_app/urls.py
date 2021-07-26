from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import ObtainAuthToken
from user_app import views

urlpatterns = [
    path('login/',ObtainAuthToken.as_view(),name='login'),
    path('register/',views.regiser_user,name='register'),
    path('logout/',views.logout_view,name='logout'),
]
