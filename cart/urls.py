from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('detail', views.CartDetailView.as_view(), name='cart-detail'),
    path('add/<int:pk>', views.CartAddView.as_view(), name='cart-add'),
    path('delete/<str:id>', views.CartDeleteView.as_view(), name='cart-delete'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('order/create', views.OrderCreationView.as_view(), name='order-create'),
    path('apply/discount/<int:pk>', views.DiscountCodeView.as_view(), name='apply-discount'),
    path('send-request/<int:pk>', views.SendRequestView.as_view(), name='send-request'),
    path('verify/', views.verify, name='verify-request'),
    path('wishlist', views.WishListDetailView.as_view(), name='wishlist'),
    path('wishlist/add/<int:pk>', views.WishListAddView.as_view(), name='wishlist-add'),
    path('wishlist/delete/<int:product_id>/', views.WishListDeleteView.as_view(), name='wishlist-delete'),
    path('wishlist/delete/<int:product_id>/<str:size>/', views.WishListDeleteView.as_view(), name='wishlist-delete-size'),
]
