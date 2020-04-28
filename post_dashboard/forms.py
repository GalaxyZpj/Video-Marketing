from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from core.models import Post

class UserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'mobile', 'email', 'username', 'password1', 'password2']


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user', None)
         super(PostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        exclude = ['user', 'thumbnail', 'created', 'modified', ]
