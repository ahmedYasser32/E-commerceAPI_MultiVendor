from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

schema_view = get_schema_view(
   openapi.Info(
      title="Multi Vendor E-Commerce API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   authentication_classes = [SessionAuthentication,TokenAuthentication],
   permission_classes     = [permissions.AllowAny],
)
from rest_framework_simplejwt.views import (TokenObtainPairView,
    TokenRefreshView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('Accounts.urls')),
    path('api/shopping/', include('shopping.urls')),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   # path('api/access token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
]
