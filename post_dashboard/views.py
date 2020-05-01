from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.template import Template, RequestContext
from django.http import HttpResponse

from core.models import *
from .forms import *
from .filters import PostFilter


class Login(LoginView):
    pass

def signup(request):
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Registration successful. Please login to continue.")
            return redirect(reverse('login'))
    return render(request, 'authentication/auth.html', { 'form': form })


class PostView(ListView):
    model = Post
    paginate_by = 12
    template_name = 'post/posts.html'
    context_object_name = 'posts'
    filterset_class = PostFilter

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['cat_all'] = Category.objects.all().order_by('name')
        context['filter'] = self.filterset_class
        context['post_type'] = self.request.path.split('/')[2]
        return context
    
    def get_queryset(self):
        post_types = ['webinar', 'video', 'upcoming']
        filter_data = {}
        if self.request.user.is_authenticated and self.request.path == reverse('dashboard'):
            filter_data['user_id'] = self.request.user.id
            if self.request.GET.get('type', None) != None:
                filter_data['type'] = self.request.GET.get('type')
        else:
            filter_data['type'] = self.request.path.split('/')[2]
            if filter_data['type'] not in post_types:
                return Post.objects.none()
        return self.filterset_class(self.request.GET, queryset=Post.objects.filter(**filter_data).order_by('-created')).qs.distinct()

def send_sub_categories_ajax(request):
    category_id = request.GET.get('category_id', None)
    for_filter = request.GET.get('filter', None)

    if category_id:
        sub_categories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    else:
        sub_categories = SubCategory.objects.all().order_by('name')
    if for_filter:
        template = Template('{% for subcat in sub_categories %}<a class="subcat-name" value="{{ subcat.id }}">{{ subcat.name }}</a>{% endfor %}')
    else:
        template = Template('<option value="" selected>---------</option>{% for sub_category in sub_categories %}<option value="{{ sub_category.id }}">{{ sub_category.name }}</option>{% endfor %}')
    return HttpResponse(template.render(RequestContext(request, { 'sub_categories': sub_categories })))

@login_required
def add_post_ajax(request):
    if request.method == 'GET':
        categories = Category.objects.all().order_by('name')
        return render(request, 'post/add_post.html', { 'categories': categories })
    elif request.method == 'POST':
        form_data = {
            'type': request.POST['type'],
            'category_id': request.POST['category'],
            'sub_category_id': request.POST['sub_category'],
            'title': request.POST['title'],
            'description': request.POST['description'],
            'date': request.POST['date'],
            'tags': request.POST['tags'],
            'video': request.POST['video'],
        }
        Post.objects.create(user=request.user, **form_data)
        return redirect(reverse('dashboard'))

def visitor_form_ajax(request, post_id):
    if request.method == 'POST':
        formData = {
            'company_agent': get_user_model().objects.get(id=request.POST['company_agent']),
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'mobile': request.POST['mobile'],
        }
        Visitor.objects.create(**formData)
        video = Post.objects.get(pk=post_id)
        return render(request, 'post/video.html', { 'post': video })
    return render(request, 'post/visitor_form.html', {
        'post': Post.objects.get(id=post_id),
    })
