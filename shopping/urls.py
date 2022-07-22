from shopping.Views.ItemViews  import ItemPost,ItemGet,ItemDelete
from shopping.Views.OrderViews import OrderedItemCreate, GetOrder,Checkout
from django.urls import path



urlpatterns = [

    path('item/Create',ItemPost.as_view()),
    path('item/Delete/<int:id>',ItemDelete.as_view()),
    path('GetItem/<int:id>',ItemGet.as_view()),
    path('GetItems/',ItemGet.as_view()),
    path('AddItemToCart/',OrderedItemCreate.as_view()),
    path('GetOrder/<int:id>',GetOrder.as_view()),
    path('Checkout/',Checkout.as_view())



]
