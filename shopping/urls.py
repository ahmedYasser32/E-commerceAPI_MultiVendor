from shopping.Views.ItemViews  import ItemPost,ItemGet,ItemDelete
from shopping.Views.OrderViews import OrderedItemCreate, GetCart
from django.urls import path



urlpatterns = [

    path('item/Create',ItemPost.as_view()),
    path('item/Delete/<int:id>',ItemDelete.as_view()),
    path('GetItem/<int:id>',ItemGet.as_view()),
    path('GetItems/',ItemGet.as_view()),
    path('AddItemToCart/',OrderedItemCreate.as_view()),
    path('GetCart/<int:id>',GetCart.as_view()),



]
