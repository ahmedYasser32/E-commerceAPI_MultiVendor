from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
    TokenRefreshView)

from Accounts.views import RegisterAPI,UserLogin,VendorCreate,CustomerCreate,Customerget,Vendorget







urlpatterns = [

    path('register/',         RegisterAPI.as_view()),
    path('Login/',            UserLogin.as_view()),
    path('PostVendor/',       VendorCreate.as_view()),
    path('PostCustomer/',     CustomerCreate.as_view()),
    path('GetVendor/<int:id>',        Vendorget.as_view()),
    path('GetCustomer/<int:id>',      Customerget.as_view()),

]

"""

from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes),
    path('notes/', views.getNotes),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
"""
