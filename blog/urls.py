from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('post/list', views.PostListView.as_view(), name='post-list'),
    path('post/detail/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('search', views.BlogSearchView.as_view(), name='blog-search')

]


