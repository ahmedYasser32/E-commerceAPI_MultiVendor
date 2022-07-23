from django.urls import path
from Accounts.views import RegisterAPI,UserLogin,VendorCreate,CustomerCreate,Customerget,Vendorget, user_verification, check_verification_mail







urlpatterns = [

    path('register/',         RegisterAPI.as_view()),
    path('Login/',            UserLogin.as_view()),
    path('PostVendor/',       VendorCreate.as_view()),
    path('PostCustomer/',     CustomerCreate.as_view()),
    path('GetVendor/<int:id>',        Vendorget.as_view()),
    path('GetCustomer/<int:id>',      Customerget.as_view()),
    path('verification',      user_verification),
    path('resend_verification',      check_verification_mail),

]


