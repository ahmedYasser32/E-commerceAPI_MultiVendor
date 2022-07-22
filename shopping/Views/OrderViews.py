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
from Accounts.models import Vendor,Customer
from shopping.models import Item,OrderItem,Order
from shopping.serializers import OrderedItemSerializer,OrderedItemSerializerList
from rest_framework_simplejwt.authentication import JWTAuthentication

class OrderedItemCreate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class   = OrderedItemSerializer
    @swagger_auto_schema(request_body=openapi.Schema(operation_description="API to add an item to user cart or alter an item that is already in a user cart",
     type=openapi.TYPE_OBJECT,
     properties={
        'id'  : openapi.Schema(type=openapi.TYPE_INTEGER , description='Item PK'),
        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER  , description='quantity of item'),
        'action':openapi.Schema(type=openapi.TYPE_STRING  , description=' send add or remove, to add or remove quantity of this item'),

     }), responses={201: OrderedItemSerializer, 400 : 'Bad Request'})
    def post(self, request, *args, **kwargs):
        print(f'\n{request.data}')

        context={}


        if(request.user.is_vendor==True):
            context['error_message'] = 'Restricted access'
            context['response'] = 'error'
            return Response(data=context)
        #print(request.user)
        customer = request.user.customer



        #print("1",Currentorder)
        #get customerOrder object
        CustomerOrders =Order.objects.filter(customer=customer)
        print("2",CustomerOrders)

        #if there is a customer order not complete, get it and add order items to it,
        # if not create object with a customer, save it and get it
        if CustomerOrders:
            for i in CustomerOrders:
                print(i.complete)
                if(i.complete==False):
                    Currentorder = i
                    break
                else:
                    Currentorder = Order.objects.create(customer=customer)
                    Currentorder = Currentorder.save()
                    Currentorder = Currentorder.objects.all().first()

        print("after loop",Currentorder)
        itemId         = request.data.get('id')
        print("after itemId  ",  itemId)


        items           = Item.objects.filter(pk=itemId)
        print("after item  ",  items)

        #Check if item exists if not return error.
        if (len(items)<0):

            context['error_message'] = 'Item does not exist'
            context['response'] = 'error'
            return Response(data=context)

        item  =  items[0]
        print("after   item  ",  item)
        itemorderitems = item.orderitem_set.all()
        print(itemorderitems)

        orderItem, created = OrderItem.objects.get_or_create(order = Currentorder, item=item)
        print("after orderItem ",  orderItem)

        print(created)

        data          = request.data.copy()


        if data['action']  == 'add':

            orderItem.quantity = (orderItem.quantity +  data['quantity'])
            if(orderItem.quantity>orderItem.item.quantity):
                print("Here quantity check")
                context['error_message'] = 'Item quantity you entered is more than the avaliable quantity'
                context['response'] = 'error'
                return Response(data=context)




        elif data['action'] == 'remove':
            orderItem.quantity = (orderItem.quantity -  data['quantity'])
            if(orderItem.quantity<0):
                  orderItem.quantity=0



        if created:
            orderItem.save()
            serializer = self.serializer_class(orderItem)
            context             = {**context, **serializer.data}
            context['response'] ='success'
            return Response(data=context)



        data['quantity'] = orderItem.quantity
        serializer = self.serializer_class(orderItem,data=data,partial=True)

        if serializer.is_valid():
            serializer.save()
            context = {**context, **serializer.data.copy()}
            context['response'] = "success"
            return Response(data=context)


        context = serializer.errors.copy()
        context['response'] = 'error'
        return Response(data=context)


class GetCart(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = OrderedItemSerializerList
    @swagger_auto_schema(operation_description=" Order id in the url to get the response   response example:",
                     responses={200: serializer_class, 400: 'Bad Request'})
    def get(self, request,id):

        context={}
        Carts = Order.objects.filter(pk=id)

        if Carts.count() == 0:
            context['response'] = 'error'
            context['error'] = 'Item doesnt exist'
            return Response(data=context)

        Cart = Carts[0]
        OrderedItems =Cart.orderitem_set.all()

        serializer          = self.serializer_class(OrderedItems,many=True)

        context['OrderedItems']  = serializer.data
        context['ItemsQuantity'] = Cart.get_cart_quantity
        context['TotalPrice']    = Cart.get_cart_total
        context['OrderStatus']   = Cart.get_order_status
        context['response']      ='success'

        return Response(data=context)

class Checkout(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = OrderedItemSerializer
    @swagger_auto_schema(request_body=openapi.Schema(operation_description="API to Check Out",
     type=openapi.TYPE_OBJECT,
     properties={
        'Orderid'  : openapi.Schema(type=openapi.TYPE_INTEGER , description='Order PK'),
        'transaction_id': openapi.Schema(type=openapi.TYPE_INTEGER  , description='quantity of item'),
     }), responses={201: OrderedItemSerializer, 400 : 'Bad Request'})

    def post(self,request):

        context={}

        id             = request.data.get('Orderid')
        transaction_id = request.data.get('transaction_id')

        Carts = Order.objects.filter(pk=id)

        if Carts.count() == 0:
            context['response'] = 'error'
            context['error'] = 'Item doesnt exist'
            return Response(data=context)

        Cart = Carts[0]
        OrderedItems        = Cart.orderitem_set.all()

        for OrderedItem in OrderedItems :
            item             =      OrderedItem.item
            item.quantity    =      item.quantity - OrderedItem.quantity
            item.save()

        Cart.transaction_id = transaction_id

        serializer          = self.serializer_class(OrderedItems,many=True)

        context['OrderedItems']     = serializer.data
        context['ItemsQuantity']    = Cart.get_cart_quantity
        context['TotalPrice']       = Cart.get_cart_total
        context['OrderStatus']      = Cart.get_order_status
        context['transaction_id']   = transaction_id
        context['response']      ='success'

        return Response(data=context)















