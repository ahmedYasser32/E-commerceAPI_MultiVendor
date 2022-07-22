from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from Accounts.models import Account,Vendor,Customer
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from Accounts.serializers import RegistrationSerializer,MyTokenObtainPairSerializer, CustomerSerializer,VendorSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication



#A class to register your account
class RegisterAPI(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegistrationSerializer
    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING , description='email'),
        'firstname': openapi.Schema(type=openapi.TYPE_STRING , description='firstname'),
        'lastname': openapi.Schema(type=openapi.TYPE_STRING , description='lastname'),
        'password': openapi.Schema(type=openapi.TYPE_STRING  , description='password'),
         'is_vendor': openapi.Schema(type=openapi.TYPE_BOOLEAN  , description='true if it is a vendor false if customer')
     }),
     responses={201: RegistrationSerializer, 400 : 'Bad Request'})

    def post(self, request, *args, **kwargs):
        print(f'\n{request.data}')
        print(request.data.get('email'))
        context = {}
        email = request.data.get('email')


       #check email if already exist send error

        if Account.objects.filter(email=email).count()>0:
            context['error_message'] = 'That email is already in use.'
            context['response'] = 'error'
            return Response(data=context)


       # Assign serializer
        serializer = self.serializer_class(data=request.data)


        if serializer.is_valid():




            #if valid save object and send response
            account = serializer.save()


            context['email'] = account.email
            context['firstname'] = account.firstname
            context['lastname'] = account.lastname
            context['pk'] = account.pk
            context['isvendor'] = account.is_vendor

            context['response'] = 'success'
            return Response(data=context)




        #if not valid return error
        context = serializer.errors.copy()
        context['response'] = 'error'
        return Response(data=context)

#Login and gain jwt access and refresh tokens
class UserLogin(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


#Build the customer profile with the customer data, accessed with jwt access token that is gained by logging in
class CustomerCreate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = CustomerSerializer
    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING , description='email'),
        'address': openapi.Schema(type=openapi.TYPE_STRING , description='address'),
        'city': openapi.Schema(type=openapi.TYPE_STRING , description='city'),
        'state': openapi.Schema(type=openapi.TYPE_STRING  , description='state'),
        'zipcode': openapi.Schema(type=openapi.TYPE_INTEGER  , description='zipcode'),
        'AdditionalInf': openapi.Schema(type=openapi.TYPE_STRING  , description='additional inf') ,

     }),
     responses={201: CustomerSerializer, 400 : 'Bad Request'})
    def post(self, request, *args, **kwargs):
        print(f'\n{request.data}')
        print(request.data.get('email'))
        context         = {}
        email           = request.data.get('email')
        is_vendor       = request.data.get('is_vendor')
        print(is_vendor)
        account         = Account.objects.filter(email=email)
        print(account)

        if account.count() == 0 :
            context['error_message'] = 'Account not found.'
            context['response'] = 'error'
            return Response(data=context)
        print("before if is_vendor: ")
        if(request.user.is_vendor):
            context['error_message'] = 'Restricted access'
            context['response'] = 'error'
            print("Inside  if is_vendor:")
            return Response(data=context)
        print("After if is_vendor :")



        account = account[0]
        data    = request.data.copy()
        #set relation
        data['account'] = account.pk
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():

            #if valid save object and send response
            serializer.save()


            context['email'] = account.email
            context['firstname'] = account.firstname
            context['lastname'] = account.lastname
            context['pk'] = account.pk
            context['response'] = 'success'
            return Response(data=context)

        #if not valid return error
        context = serializer.errors.copy()
        context['response'] = 'error'
        return Response(data=context)

    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING , description='email'),
        'address': openapi.Schema(type=openapi.TYPE_STRING , description='address'),
        'city': openapi.Schema(type=openapi.TYPE_STRING , description='city'),
        'state': openapi.Schema(type=openapi.TYPE_STRING  , description='state'),
        'zipcode': openapi.Schema(type=openapi.TYPE_INTEGER  , description='zipcode'),
        'AdditionalInf': openapi.Schema(type=openapi.TYPE_STRING  , description='additional inf') ,
        'id': openapi.Schema(type=openapi.TYPE_INTEGER  , description='zipcode'),

     }),
     responses={201: CustomerSerializer, 400 : 'Bad Request'})
    def put(self, request):
        print(f'\n{request.data}')
        context         = {}
        if(request.user.is_vendor):
            context['error_message'] = 'Restricted access'
            context['response'] = 'error'
            return Response(data=context)

        account = request.user
        id      = request.data.get('id')


        customer = Customer.objects.filter(pk=id)

        if customer.count() == 0:
            context['response'] = 'error'
            context['error'] = 'Item doesnt exist'
            return Response(data=context)

        customer_detail = customer[0]
        data=request.data.copy()
        data['modified_at'] = dt.datetime.now()
        serializer = self.serializer_class(customer_detail,data=data,partial=True)
             #check if data valid or there is an exception
        if serializer.is_valid():
            serializer.save()
            context = {**context, **serializer.data.copy()}
            context['response'] = "success"
            return Response(data=context)

        else:
            context = serializer.errors.copy()
            context['response'] = 'error'
            return Response(data=context)



#Build the Vendor profile with the Vendor data, accessed with jwt access token that is gained by logging in,Get vendor,
class VendorCreate(APIView):

    authentication_classes  = [JWTAuthentication]
    permission_classes  = [IsAuthenticated,]

    permission_classes = [IsAuthenticated,]
    serializer_class = VendorSerializer
    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING , description='email'),
        'brand': openapi.Schema(type=openapi.TYPE_STRING , description='brand'),
        'about': openapi.Schema(type=openapi.TYPE_STRING , description='about'),
        'rating': openapi.Schema(type=openapi.TYPE_INTEGER  , description='rating'),

     }),
     responses={201: VendorSerializer, 400 : 'Bad Request'})
    def post(self, request, *args, **kwargs):
        print(f'\n{request.data}')
        print(request.data.get('email'))
        context         = { }
        email           = request.data.get('email')
        #is_vendor       = request.data.get('is_vendor')
        account         = Account.objects.filter(email=email)
        print(account)

        if account.count() == 0 :
            context['error_message'] = 'Account not found.'
            context['response'] = 'error'
            return Response(data=context)

        if(request.user.is_vendor == False):

            context['error_message'] = 'Restricted access'
            context['response'] = 'error'
            return Response(data=context)

        account = account[0]
        data    = request.data.copy()
        #set relation
        data['account'] = account.pk
        serializer = self.serializer_class(data=data)


        if serializer.is_valid():

            #if valid save object and send response
            serializer.save()
            context['email']    = account.email
            context['brand']    = data['brand']
            context['pk']       = account.pk
            context['response'] = 'success'
            return Response(data=context)

        #if not valid return error
        context = serializer.errors.copy()
        context['response'] = 'error'
        return Response(data=context)
    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING , description='email'),
        'brand': openapi.Schema(type=openapi.TYPE_STRING , description='brand'),
        'about': openapi.Schema(type=openapi.TYPE_STRING , description='about'),
        'rating': openapi.Schema(type=openapi.TYPE_INTEGER  , description='rating'),
        'id': openapi.Schema(type=openapi.TYPE_INTEGER  , description='id'),
        #'is_vendor': openapi.Schema(type=openapi.TYPE_BOOLEAN  , description='is_vendor')

     }),
     responses={201: VendorSerializer, 400 : 'Bad Request'})
    def put(self, request):
        print(f'\n{request.data}')
        context         = {}
        if(request.user.is_vendor == False):

            context['error_message'] = 'Restricted access'
            context['response'] = 'error'
            return Response(data=context)

        account = request.user
        id      = request.data.get('id')


        vendor = Vendor.objects.filter(pk=id)

        if vendor.count() == 0:
            context['response'] = 'error'
            context['error'] = 'Item doesnt exist'
            return Response(data=context)

        vendor_detail = vendor[0]
        data=request.data.copy()
        data['modified_at'] = dt.datetime.now()
        serializer = self.serializer_class(vendor_detail,data=data,partial=True)
             #check if data valid or there is an exception
        if serializer.is_valid():
            serializer.save()
            context = {**context, **serializer.data.copy()}
            context['response'] = "success"
            return Response(data=context)

        else:
            context = serializer.errors.copy()
            context['response'] = 'error'
            return Response(data=context)




class Vendorget(APIView):

        serializer_class = VendorSerializer


        @swagger_auto_schema(operation_description=" Vendor id in the url to get the response ",
                         responses={201: serializer_class, 400: 'Bad Request'})

        def get(self, request,id):
            context = {}
            vendor = Vendor.objects.filter(pk=id)
            if vendor.count() == 0:
                context['response'] = 'error'
                context['error'] = 'Vendor doesnt exist'
                return Response(data=context)

            vendor_detail = vendor[0]
            serializer          = self.serializer_class(vendor_detail)
            context             = {**context, **serializer.data}
            context['response'] ='success'
            return Response(data=context)



class Customerget(APIView):

        serializer_class = CustomerSerializer


        @swagger_auto_schema(operation_description=" Customer id in the url to get the response ",
                         responses={201: serializer_class, 400: 'Bad Request'})
        def get(self, request,id):
            context={}
            customer = Customer.objects.filter(pk=id)
            if customer.count() == 0:
                context['response'] = 'error'
                context['error'] = 'Vendor doesnt exist'
                return Response(data=context)

            customer_detail = customer[0]
            serializer          = self.serializer_class(customer_detail)
            context             = {**context, **serializer.data}
            context['response'] ='success'
            return Response(data=context)






