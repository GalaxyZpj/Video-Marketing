from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('user/dashboard/', login_required(PostView.as_view()), name='dashboard'),
    path('posts/<str:post_type>/', PostView.as_view(), name='posts'),
    path('add_post/', add_post_ajax, name='addPost'),
    path('sub_category/', send_sub_categories_ajax, name='sub-category'),
    path('visitor/<slug:post_id>', visitor_form_ajax, name='visitor-form'),
]
