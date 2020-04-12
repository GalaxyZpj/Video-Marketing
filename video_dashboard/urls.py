from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard/', video_dashboard, name='dashboard'),
    path('video', videos, name='videos'),
    path('play/<slug:video_id>', play_video, name='play'),
    path('add_post/', add_post, name='addPost'),
]
