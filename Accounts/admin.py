from django.contrib import admin
from Accounts.models import Account,Customer,Vendor
from shopping.models import Item,OrderItem,Order
# Register your models here.



class AccountAdmin(admin.ModelAdmin):
    list_display = ('email','firstname','lastname')
    search_fields = ('pk', 'email','firstname', 'lastname')
    readonly_fields=('pk', 'date_joined', 'last_login')

admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Account,AccountAdmin)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
