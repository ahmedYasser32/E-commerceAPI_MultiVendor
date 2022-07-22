from rest_framework import serializers
from Accounts.models import Account,Customer,Vendor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        # The client should not be able to send a token along with a registration
         # request. Making `token` read-only handles that for us.

        fields = ['email', 'firstname', 'lastname', 'password', 'is_staff',  'verified','is_vendor']
        extra_kwargs = {
                'password': {'write_only': True, 'min_length': 8, 'max_length': 50},
        }


    def	save(self) :

        account = Account(
            email=self.validated_data['email'],
            firstname=self.validated_data['firstname'],
            lastname=self.validated_data['lastname'],
            is_vendor=self.validated_data['is_vendor']
                )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    class Meta:
        model = Account
        fields = ['email', 'firstname', 'lastname', 'password', 'is_staff',  'verified','token']

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.firstname



        return token

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
         model = Customer
         fields='__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
         model = Vendor
         fields='__all__'
