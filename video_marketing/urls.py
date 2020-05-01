from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from post_dashboard.views import Login

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('login/', Login.as_view(template_name='authentication/auth.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('', include('post_dashboard.urls')),
]
