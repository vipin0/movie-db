
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Movie Database API",
      default_version='v1',
      description="A sample Movie Database API",
      terms_of_service="http://localhost:8000",
      contact=openapi.Contact(email="vipin@selfcode.in"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('api.urls')),
    path('api-auth',include('rest_framework.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
