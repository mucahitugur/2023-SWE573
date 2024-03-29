from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    UserProfileView,
    MyProfileView,
    follow,
    search,
    post_detail,
    like_post,
    add_comment,
    PostsView,  # make sure to import this
)

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/new/', BlogCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('profile/', MyProfileView.as_view(), name='my_profile'),
    path('follow/<str:username>/', follow, name='follow_user'),
    path('search/', search, name='search'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('posts/tag/<slug:tag_slug>/', PostsView.as_view(), name='posts_by_tag'),
]
