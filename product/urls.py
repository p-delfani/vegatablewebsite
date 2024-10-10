from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('list', views.ProductListView.as_view(), name='product-list'),
    path('detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('category/<int:pk>', views.CategoryProductView.as_view(), name='category-product')
]
