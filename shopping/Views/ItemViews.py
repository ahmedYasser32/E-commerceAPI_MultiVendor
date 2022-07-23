from rest_framework.parsers import MultiPartParser, JSONParser
from django.db.models import Case, When, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from rest_framework.decorators import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView
import datetime as dt
from Accounts.models import Vendor
from shopping.models import Item
from shopping.serializers import PostItemSerializer,GetItemSerializer, PictureSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication





class ItemPost(APIView):

    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated,]
    serializer_class        = PostItemSerializer
    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING , description='Item name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING , description='Item description'),
        'category': openapi.Schema(type=openapi.TYPE_STRING , description='category choose one, send char'),
        'types': openapi.Schema(type=openapi.TYPE_STRING  , description='types choose one, send char'),
        'price': openapi.Schema(type=openapi.TYPE_INTEGER  , description='price'),
        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER  , description='quantity of item'),

     }),
     responses={201: serializer_class , 400 : 'Bad Request'})
    def post(self, request, *args, **kwargs):
        print(f'\n{request.data}')
        context         = { }
        if(request.user.is_vendor == False):

            context['error_message'] = 'Restricted access'
            context['response'] = 'error'
            return Response(data=context)



        data=request.data.copy()
        data['vendor'] = request.user.vendor
        data['created_at'] = dt.datetime.now()

        serializer = self.serializer_class(data=data)


        if serializer.is_valid():
            serializer.save()
            context = {**context, **serializer.data.copy()}
            context['response'] = "success"

            return Response(data=context)


        context = serializer.errors.copy()
        context['response'] = 'error'
        return Response(data=context)



    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
        'id'  : openapi.Schema(type=openapi.TYPE_STRING , description='Item PK'),
        'name': openapi.Schema(type=openapi.TYPE_STRING , description='Item name'),
        'description': openapi.Schema(type=openapi.TYPE_STRING , description='Item description'),
        'category': openapi.Schema(type=openapi.TYPE_STRING , description='category choose one, send char'),
        'types': openapi.Schema(type=openapi.TYPE_STRING  , description='types choose one, send char'),
        'price': openapi.Schema(type=openapi.TYPE_INTEGER  , description='price'),
        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER  , description='quantity of item'),

     }),
     responses={201: serializer_class , 400 : 'Bad Request'})
    def put(self, request):
        print(f'\n{request.data}')
        context         = {}
        if(request.user.is_vendor == False):

            context['error_message'] = 'Restricted access'
            context['response'] = 'error'
            return Response(data=context)

        account = request.user
        id      = request.data.get('id')


        item = Item.objects.filter(pk=id)

        if item.count() == 0:
            context['response'] = 'error'
            context['error'] = 'Item doesnt exist'
            return Response(data=context)

        Item_detail = item[0]

       #Check if  the vendor requesting is the owner of this product to edit it or not if not response is error: Restricted access
        if(account.vendor==Item_detail.vendor):
             data=request.data.copy()
             data['vendor'] = request.user.vendor
             data['modified_at'] = dt.datetime.now()
             serializer = self.serializer_class(Item_detail,data=data,partial=True)
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



        else:
            context['error_message'] = 'Restricted access'
            context['response'] = 'error'
            return Response(data=context)

class ItemGet(APIView):
    authentication_classes  = []
    permission_classes      = []
    serializer_class        = GetItemSerializer
    @swagger_auto_schema(operation_description=" Item id in the url to get the response ",
                         responses={201: serializer_class, 400: 'Bad Request'})
    def get(self, request, id):

        context={}
        item = Item.objects.filter(pk=id)

        if item.count() == 0:
            context['response'] = 'error'
            context['error'] = 'Item doesnt exist'
            return Response(data=context)

        Item_detail = item[0]

        serializer          = self.serializer_class(Item_detail)
        context             = {**context, **serializer.data}
        context['response'] ='success'
        return Response(data=context)


class ItemGetList(APIView):
    authentication_classes  = []
    permission_classes      = []
    serializer_class        = GetItemSerializer
    @swagger_auto_schema(operation_description=" Item id in the url to get the response ",
                         responses={201: serializer_class, 400: 'Bad Request'})
    def get(self, request, id):

        context={}
        item = Item.objects.filter(pk=id)

        if item.count() == 0:
            context['response'] = 'error'
            context['error'] = 'Item doesnt exist'
            return Response(data=context)

        Item_detail = item[0]

        serializer          = self.serializer_class(Item_detail)
        context             = {**context, **serializer.data}
        context['response'] ='success'
        return Response(data=context)


    @swagger_auto_schema(operation_description="returns a list of items,if you entered filters or sorting they will be filtered and "
    "sorted , filters are ?category= (M forMen WM for Women K for Kids) choose a letter after =, you can add another filters like this "
    "?category=K&type=(You can choose a type C fror casual FM for formal and SP for Sport you can also choose a sorting by  sortby= price or quantity or leave it to defaul, by newest"
    "You can also filter by price range by sending lowPrice=  and highPrice= the words and values must be sent just like I typed them here"
    "URl Example :  api/shopping/GetItems/?category=&type=&brand=&sortby=&lowPrice=&highPrice= /"
                                               "Put the values after=",
                         responses={200: serializer_class, 400: 'Bad Request'})
    def get(self, request):

        filters   = []
        context={}

        filter_category = request.GET.get('category')
        filter_type     = request.GET.get('type')
        filter_vendor   = request.GET.get('brand')
        sortby          = request.GET.get('sortby') #price/quantity/created_at
        lowPrice        = request.GET.get("lowPrice")
        highPrice       = request.GET.get("highPrice")
        items = Item.objects.all()


        if highPrice and lowPrice:
          print("HIGH and low")
          qprice =  Q ( Q(price__lte=highPrice ) & Q( price__gte=lowPrice) )
          filters.append(qprice)



        if filter_type:
            print("Type filter :"+ filter_type)
            Qfilter_type = Q(types=filter_type)
            filters.append(Qfilter_type)

        if filter_category:
            print("filter_category :"+ filter_category)
            qfilter_category = Q(category=filter_category)
            filters.append(qfilter_category)


        if filter_vendor:
            vendor = Vendor.objects.filter(brand=filter_vendor)
            if vendor:
                print("filter_vendor:")
                VendorObject  = vendor[0]
                vendorId      = VendorObject.pk
                qvendor       = Q(vendor=vendorId)
                filters.append(qvendor)


            elif len(filters)==1 :
                print("NOT filter_vendor:")
                context['response'] = 'error'
                context['error'] = 'brand doesnt exist or dosent have items yet '





        print("after filters conditions",len(filters))
        if sortby:
            print("in sort by :", sortby)
            sortby = sortby
        else:
            sortby = 'created_at'
            print("in sort by :", sortby)










        if len(filters)<0:
            print("In filters",len(filters))

            items = Item.objects.all().order_by(sortby)

        else:

            for i in filters:

                print("inside loop")
                items = items.filter(i).order_by(sortby)
                items = items

                print(i)
                print(items)
            print("outside loop")


        if items.count() == 0:
            context['response'] = 'error'
            context['error'] = 'Item doesnt exist'
            return Response(data=context)


        serializer          = self.serializer_class(items, many=True)
        context['items']     = serializer.data
        context['response'] ='success'
        return Response(data=context)


class ItemDelete(APIView):

    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated,]

    @swagger_auto_schema(operation_description=" Item id to delete it, ignore in post and put , delete only  ",
                         responses={204: None, 400: 'Bad Request'})
    def delete(self, request, id):


        item = Item.objects.filter(pk=id)

        if item.count() == 0:
            context={}
            context['response'] = 'error'
            context['error'] = 'Item doesnt exist'
            return Response(data=context)

        Item_detail = item[0]


        Item_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class PictureUploadView(APIView):

    permission_classes = [IsAuthenticated]
    parser_class = (MultiPartParser, JSONParser)



    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
     'picture' :  openapi.Schema(type=openapi.TYPE_FILE , description='.pdf or imgs '),
     }),
     responses={201: PictureSerializer , 400 : 'Bad Request'})
    def put(self, request, id, *args, **kwargs):

        context={}
        item = Item.objects.filter(id = id, vendor__account_id=request.user.pk).first()

        if not item:
            context['response'] = 'Error'
            context['error_message'] = 'item not found'
            return Response(data=context)



        context['picture'] = request.FILES.get('picture')

        file_serializer = PictureSerializer(item ,data=context)

        if file_serializer.is_valid():

            file_serializer.save()
            context = file_serializer.data.copy()

            context['response']    = "Success"
            return Response(data= context, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




