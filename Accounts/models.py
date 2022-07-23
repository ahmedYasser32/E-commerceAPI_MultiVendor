import math
import random
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')


        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= None
    firstname               = models.CharField(max_length=25,null = False,default="firstname")
    lastname                = models.CharField(max_length=25,null = False,default="lastname")
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    #add boolean field to differentiate between users and Vendors
    is_vendor				= models.BooleanField(default=False)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    verified                = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def verify(self):
        from SpreeTask.tasks import  SendVerificationMail
        email = self.email

        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        codes = AccountCode.objects.filter(user=self.pk)
        if codes.count() == 0:
            codes = AccountCode.objects.create(user=self, verification_code=OTP)
        else:
            codes = codes[0]
        codes.verification_code = OTP
        codes.save()
        subject = f'hi {self.firstname}, this mail is for your verification code:'
        # body = f'your verification code is: {codes.verification_code}'
        SendVerificationMail(subject=subject, to=email, code=codes.verification_code).start()



    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True







class Customer(models.Model):

    account        = models.OneToOneField(Account,on_delete=models.CASCADE,primary_key=True,)
    address        = models.CharField(max_length=200, null=False)
    city           = models.CharField(max_length=200, null=False)
    state          = models.CharField(max_length=200, null=False)
    zipcode        = models.CharField(max_length=200, null=False)
    date_added     = models.DateTimeField(auto_now_add=True)
    AdditionalInf  = models.CharField(max_length=200,null=True)


class Vendor(models.Model):

    account          = models.OneToOneField(Account,on_delete=models.CASCADE,primary_key=True,)
    brand            = models.CharField(max_length=50)
    about            = models.CharField(max_length=500)
    rating           = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)

class AccountCode(models.Model):
	user              = models.OneToOneField(Account, on_delete=models.CASCADE)
	verification_code = models.CharField(max_length=6, null=False, blank=False)

