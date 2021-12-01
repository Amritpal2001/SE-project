from django.urls import path
from .views import (PostListView, 
                    PostDetailView , 
                    PostCreateView , 
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
                    addRating,
                    )
from . import views 
urlpatterns = [
    path('', PostListView , name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view() , name='user-posts'),
    path('post/<int:id>/', PostDetailView , name='post-detail'),
    path('post/new/', PostCreateView.as_view() , name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view() , name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view() , name='post-delete'),
    path('about/', views.about , name='blog-about'),
    path('addRating/', addRating , name='addRating'),
]
