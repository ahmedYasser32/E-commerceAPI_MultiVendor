import os
from uuid import uuid4
from django.db import models
from Accounts.models  import Account,Customer,Vendor
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


def image_upload_path(instance, filename):
    upload_to = 'media/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.name:
        filename = '{}.{}'.format(instance.name, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Item(models.Model):

  Categories    =  [("M","Men"),("WM","Women"),("K","Kids")]
  Types         =   [("C","Casual"),("FR","Formal"),("SP","Sport")]
  name          = models.CharField(max_length=200)
  description   = models.CharField(max_length=500)
  created_at	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
  modified_at   = models.DateTimeField(verbose_name='date modified',null=True)
  category      = models.CharField(max_length=30,choices=Categories,default="WM")
  types         = models.CharField(max_length=30,choices=Types,default="C")
  price         = models.IntegerField(default=0, null=True, blank=True)
  quantity      = models.PositiveIntegerField(default=0, null=True, blank=True)
  vendor        = models.ForeignKey(Vendor,default=-1,on_delete=models.CASCADE)
  picture = models.ImageField(upload_to=image_upload_path, blank=True, null=True)


class Order(models.Model):


     statuses       = [(1,"preparing"),(2,"Ready"),(3,"Delivering"),(4,"Delivered"),(-1,"Cancelled"),(0,"Pending")]
     created_at	    = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
     status         = models.SmallIntegerField(choices=statuses,default=0)
     total_price    = models.PositiveIntegerField(default=0)
     isdiscount     = models.BooleanField(default=False)
     discount       = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)],default=0)
     customer       = models.ForeignKey(Customer, on_delete=models.CASCADE)
     complete       = models.BooleanField(default=False)
     transaction_id = models.CharField(max_length=10, null=True)

     @property
     def get_cart_total(self):
         orderitems = self.orderitem_set.all()
         total = sum([item.get_total for item in orderitems])
         return total

     @property
     def get_order_status(self):
         orderitems = self.orderitem_set.all()
         minimum = min([item.status for item in orderitems])

         return minimum

     @property
     def get_cart_quantity(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):

    statuses       = [(1,"Accepted"),(2,"Ready for delivery"),(3,"Delivering"),(4,"Delivered"),(-1,"Cancelled"),(0,"Pending")]
    item       = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    #costumer    = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order      = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    status         = models.SmallIntegerField(choices=statuses,default=0)
    quantity   = models.IntegerField(default=0, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    price      = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total



class Review(models.Model) :

    rating  =  models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    review  =  models.CharField(max_length=500,null=True)
    user    =  models.CharField(max_length=25)
    date    =  models.DateField(auto_now_add=True)
    product =  models.ForeignKey(Item,on_delete=models.CASCADE, blank=True)
