from django.urls import path,include
urlpatterns = [
    path('',include('movieDbApp.urls')),
    path('user/',include('user_app.urls')),
]