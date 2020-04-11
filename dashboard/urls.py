from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('video', videos, name='videos'),
    path('play/<slug:video_id>', play_video, name='play'),
]
