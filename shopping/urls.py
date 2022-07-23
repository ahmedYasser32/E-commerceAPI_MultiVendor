from shopping.Views.ItemViews  import ItemPost,ItemGet,ItemDelete,PictureUploadView,ItemGetList
from shopping.Views.OrderViews import OrderedItemCreate, GetOrder,Checkout,status
from django.urls import path



urlpatterns = [

    path('item/Create',ItemPost.as_view()),
    path('item/Delete/<int:id>',ItemDelete.as_view()),
    path('GetItem/<int:id>',ItemGet.as_view()),
    path('GetItems/',ItemGetList.as_view()),
    path('AddItemToCart/',OrderedItemCreate.as_view()),
    path('GetOrder/<int:id>',GetOrder.as_view()),
    path('Checkout/',Checkout.as_view()),
    path('upload_picture/<int:id>',PictureUploadView.as_view()),
    path('Update_status/',status.as_view()),


]
