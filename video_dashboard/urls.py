from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('dashboard/', login_required(UserDashboard.as_view()), name='dashboard'),
    path('video/', Videos.as_view(), name='videos'),
    path('filter_videos/', filter_videos, name='filter-videos'),
    path('play/<slug:video_id>', play_video, name='play'),
    path('add_post/', add_post, name='addPost'),
    path('sub_category/', send_sub_categories, name='sub-category'),
]
