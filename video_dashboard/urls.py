from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('user/dashboard/', login_required(PostView.as_view()), name='dashboard'),
    path('posts/<str:post_type>/', PostView.as_view(), name='posts'),
    path('play/<slug:video_id>', play_video, name='play'),
    path('add_post/', add_post, name='addPost'),
    path('sub_category/', send_sub_categories, name='sub-category'),
]
