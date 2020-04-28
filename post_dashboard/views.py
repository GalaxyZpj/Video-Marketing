from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.db.models import Q, QuerySet
from django.views.generic import ListView
from django.template import Template, RequestContext
from django.http import HttpResponse

from core.models import *
from .forms import *
from .filters import PostFilter


class Login(LoginView):
    pass
    # def get_success_url(self):
    #     # return super().get_success_url()
    #     # return self.get_redirect_url()
    #     return self.request.POST['next']
    # def dispatch(self, request, *args, **kwargs):
    #     if self.redirect_authenticated_user and self.request.user.is_authenticated:
    #         redirect_to = self.get_success_url()
    #         if redirect_to == self.request.path:
    #             raise ValueError(
    #                 "Redirection loop for authenticated user detected. Check that "
    #                 "your LOGIN_REDIRECT_URL doesn't point to a login page."
    #             )
    #         return HttpResponseRedirect(redirect_to)
    #     return super().dispatch(request, *args, **kwargs)

def signup(request):
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="Registration successful. Please login with your credentials")
            return redirect(reverse('login'))
    return render(request, 'authentication/auth.html', { 'form': form })


class PostView(ListView):
    model = Post
    paginate_by = 12
    template_name = 'video_dashboard/posts.html'
    context_object_name = 'posts'
    filterset_class = PostFilter

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = list(Category.objects.all().values('id', 'name'))
        categories_with_subcategories = []
        categories = Category.objects.prefetch_related('subcategory_set').all()
        for category in categories:
            obj = {}
            obj['category'] = category
            obj['sub_categories'] = category.subcategory_set.all()
            categories_with_subcategories.append(obj)
        context['sub_categories'] = list(SubCategory.objects.all().values('id', 'name'))
        context['filter'] = self.filterset_class
        context['post_type'] = self.request.path.split('/')[2]
        context['cat_all'] = categories_with_subcategories
        return context
    
    def get_queryset(self):
        post_types = ['webinar', 'video', 'upcoming']
        filter_data = {}
        if self.request.user.is_authenticated and self.request.path == reverse('dashboard'):
            print('\n\n', 'DASHBOARD')
            filter_data['user_id'] = self.request.user.id
            if self.request.GET.get('type', None) != None:
                filter_data['type'] = self.request.GET.get('type')
        else:
            print('\n\n', 'NOT DASHBOARD')
            filter_data['type'] = self.request.path.split('/')[2]
            if filter_data['type'] not in post_types:
                return Post.objects.none()
        print('\n\n', filter_data)
        return self.filterset_class(self.request.GET, queryset=Post.objects.filter(**filter_data).order_by('-created')).qs.distinct()

def send_sub_categories(request):
    category_id = request.GET.get('category_id', None)
    for_filter = request.GET.get('filter', None)

    if category_id:
        sub_categories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    else:
        sub_categories = SubCategory.objects.all().order_by('name')
    if for_filter:
        template = Template('{% for subcat in sub_categories %}<button class="subcat-name" name="sub_category" value="{{ subcat.id }}">{{ subcat.name }}</button>{% endfor %}')
    else:
        template = Template('<option value="" selected>---------</option>{% for sub_category in sub_categories %}<option value="{{ sub_category.id }}">{{ sub_category.name }}</option>{% endfor %}')
    return HttpResponse(template.render(RequestContext(request, { 'sub_categories': sub_categories })))

@login_required
def add_post(request):
    if request.method == 'GET':
        categories = Category.objects.all().order_by('name')
        return render(request, 'video_dashboard/add_post.html', { 'categories': categories })
    elif request.method == 'POST':
        form = {}
        print('\n\n', request.POST)
        form['type'] = request.POST['type']
        form['category_id'] = request.POST['category']
        form['sub_category_id'] = request.POST['sub_category']
        form['title'] = request.POST['title']
        form['description'] = request.POST['description']
        form['date'] = request.POST['date']
        form['tags'] = request.POST['tags']
        form['video'] = request.POST['video']
        Post.objects.create(user=request.user, **form)
        posts = Post.objects.filter(user=request.user).order_by('-created')
        return redirect(reverse('dashboard'))

def play_video(request, video_id):
    video = Post.objects.get(pk=video_id)
    return render(request, 'video_dashboard/video.html', { 'post': video })
