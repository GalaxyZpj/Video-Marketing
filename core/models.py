from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    COMPANY_SIZE_CHOICES = [
        ('1-10', '1-10'),
        ('11-50', '11-50'),
        ('51-200', '51-200'),
        ('200+', '200+'),
    ]
    mobile = models.CharField("Mobile", max_length=16, blank=False)
    company_name = models.CharField("Company Name", max_length=64, blank=False)
    company_size = models.CharField("Company Size", max_length=16, choices=COMPANY_SIZE_CHOICES, blank=False)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField("Category Name", max_length=64, blank=False)
    description = models.TextField("Category Description", max_length=10224, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    name = models.CharField("SubCategory Name", max_length=64, blank=False)
    description = models.TextField("SubCategory Description", max_length=10224, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'sub Categories'

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Post(models.Model):
    POST_TYPE = [
        ('webinar', 'Webinar'),
        ('video', 'Video'),
        ('upcoming', 'Upcoming'),
    ]
    type = models.CharField('Post Type', max_length=16, blank=False, choices=POST_TYPE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=False)
    title = models.CharField("Post Title", max_length=128, blank=False)
    description = models.TextField("Post Description", max_length=1024, blank=True)
    date = models.DateField("Date", blank=True, null=True)
    tags = models.TextField("Tags", max_length=1024, blank=True)
    video = models.URLField("Video URL")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.pk})"


class Visitor(models.Model):
    company_agent = models.ForeignKey(get_user_model(), related_name="visitors", on_delete=models.CASCADE, blank=False)
    first_name = models.CharField("First Name", max_length=64, blank=False)
    last_name = models.CharField("Last Name", max_length=64, blank=False)
    email = models.EmailField("Email", blank=False)
    mobile = models.CharField("Mobile", max_length=16, blank=False)

    def __str__(self):
        return self.email
