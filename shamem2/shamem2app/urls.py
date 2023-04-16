from django.urls import path, include
from .views import (BlogListView, 
                    BlogDetailView, 
                    BlogCreateView, 
                    BlogUpdateView,
                    BlogDeleteView,
                    follow,
                    UserProfileView,
                    MyProfileView,
                    search  # Change user_search to search
                    )

urlpatterns=[
    path("post/<int:pk>/silme/", BlogDeleteView.as_view(), name="post_silme"),
    path("post/<int:pk>/edit", BlogUpdateView.as_view(), name="post_edit"),
    path("post/yeni/", BlogCreateView.as_view(), name="post_yeni"),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('', BlogListView.as_view(), name='home'),
    path('users/<slug:username>/', UserProfileView.as_view(), name='user_profile'),
    path('users/<slug:username>/follow/', follow, name='follow'),
    path('myprofile/', MyProfileView.as_view(), name='my_profile'),
    path('search/', search, name='search'),  # Change user_search to search
    path('accounts/', include('accounts.urls')),
]
