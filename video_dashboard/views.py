from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.template import Template, RequestContext
from django.db.models import Q
from django.views.generic import ListView, FormView
from django_filters.views import FilterMixin, FilterView

from core.models import *
from .forms import *
from .filters import PostFilter


class Login(LoginView):
    def get_template_names(self):
        backdrop_login = self.request.GET.get('backdrop', None)
        if backdrop_login:
            return ['authentication/backdropLogin.html']
        else:
            return ['authentication/login.html']


def signup(request):
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        # return render(request, 'authentication/login.html')
    return render(request, 'authentication/signup.html', { 'form': form })


class UserDashboard(ListView):
    model = Post
    paginate_by = 9
    template_name = 'video_dashboard/index.html'
    context_object_name = 'posts'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created')


class Videos(ListView):
    model = Post
    paginate_by = 9
    template_name = 'video_dashboard/index.html'
    context_object_name = 'posts'
    filterset_class = PostFilter
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['type'] = self.request.GET.get('type')
        return context

    def get_queryset(self):
        type = self.request.GET.get('type')
        search_q = self.request.GET.get('search')
        if search_q:
            qs = Post.objects.filter(Q(title__icontains=search_q) | Q(tags__icontains=search_q)).filter(type=type).order_by('-created')
        else:
            # qs = PostFilter(self.request.GET, queryset=Post.objects.filter(type=type).order_by('-created')).qs
            self.filterset = self.filterset_class(self.request.GET, queryset=Post.objects.filter(type=type).order_by('-created'))
            # self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
            qs = self.filterset.qs.distinct()
        return qs

@login_required
def add_post(request):
    if request.method == 'GET':
        categories = Category.objects.all().order_by('name')
        return render(request, 'video_dashboard/add_post.html', { 'categories': categories })
    else:
        form = {}
        print('\n\n', request.POST)
        form['type'] = request.POST['type']
        form['category_id'] = request.POST['category']
        form['sub_category_id'] = request.POST['sub_category']
        form['title'] = request.POST['title']
        form['description'] = request.POST['description']
        form['tags'] = request.POST['tags']
        form['video'] = request.POST['video']
        Post.objects.create(user=request.user, **form)
        posts = Post.objects.filter(user=request.user).order_by('-created')
        return render(request, 'video_dashboard/index.html', {
            'posts': posts,
        })

def send_sub_categories(request):
    category_id = request.GET.get('category_id', None)
    if category_id:
        sub_categories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    else:
        sub_categories = SubCategory.objects.all().order_by('name')
    template = Template('<option value="" selected>---------</option>{% for sub_category in sub_categories %}<option value="{{ sub_category.id }}">{{ sub_category.name }}</option>{% endfor %}')
    return HttpResponse(template.render(RequestContext(request, { 'sub_categories': sub_categories })))

def play_video(request, video_id):
    video = Post.objects.get(pk=video_id)
    return render(request, 'video_dashboard/video.html', { 'post': video })

def filter_videos(request):
    if request.method == 'GET':
        type = request.GET.get('type')
        categories = Category.objects.all().order_by('name')
        sub_categories = SubCategory.objects.all().order_by('name')
        posts_filter = PostFilter(request.GET, queryset=Post.objects.filter(type=type))
        return render(request, 'video_dashboard/filter.html', { 'posts': posts_filter, 'categories': categories, 'sub_categories': sub_categories, 'type': type })
