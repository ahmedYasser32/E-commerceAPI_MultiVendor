from rest_framework import serializers
from shopping.models import Item,OrderItem,Order
from Accounts.models  import Customer,Vendor




class PostItemSerializer(serializers.ModelSerializer):

    #Vendor data that may be used in the front end


    class Meta:
         model = Item
         fields = '__all__'



class GetItemSerializer(serializers.ModelSerializer):

    #Vendor data that may be used in the front end

    vendor_email     = serializers.CharField(source='vendor.account.email')
    brand            = serializers.CharField(source='vendor.brand')
    class Meta:
         model = Item
         fields = '__all__'

class OrderedItemSerializer(serializers.ModelSerializer):
     name     = serializers.CharField(source='item.name')
     class Meta:
         model = OrderItem
         fields = '__all__'

class OrderedItemSerializerList(serializers.ModelSerializer):
     name     = serializers.CharField(source='item.name')
     class Meta:
         model = OrderItem
         fields = ('name','quantity','get_total','status')

