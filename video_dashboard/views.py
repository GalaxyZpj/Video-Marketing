from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required

from core.models import *

@login_required
def video_dashboard(request):
    categories = Category.objects.all()
    if request.method == 'GET':
        posts = Post.objects.filter(user=request.user)
        return render(request, 'video_dashboard/index.html', {
            'categories': categories,
            'posts': posts,
        })
    else:
        form = {}
        # form['category'] = request.POST['category']
        category_id = request.POST['category']
        print('\n\n\n', type(category_id))
        form['title'] = request.POST['title']
        form['description'] = request.POST['description']
        form['video'] = request.POST['video']
        video_code = form['video'].split('?v=')[1].split('&')[0]
        form['thumbnail'] = f'https://img.youtube.com/vi/{video_code}/maxresdefault.jpg'
        Post.objects.create(user=request.user, category=Category.objects.get(pk=category_id), **form)
        posts = Post.objects.filter(user=request.user)
        return render(request, 'video_dashboard/index.html', {
            'categories': categories,
            'posts': posts,
        })

def add_post(request):
    categories = Category.objects.all()
    return render(request, 'video_dashboard/add_post.html', { 'categories': categories })

def videos(request):
    posts = Post.objects.all()
    return render(request, 'video_dashboard/index.html', {
        'posts': posts,
    })

def play_video(request, video_id):
    video = Post.objects.get(pk=video_id)
    return render(request, 'video_dashboard/video.html', {"post": video})
