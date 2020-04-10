from django.db import models
from django.contrib.auth import get_user_model
from embed_video.fields import EmbedVideoField

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


class Tag(models.Model):
    name = models.CharField("Tag Name", max_length=64, blank=False)
    description = models.TextField("Tag Description", max_length=1024, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    title = models.CharField("Post Title", max_length=128, blank=False)
    description = models.TextField("Post Description", max_length=1024, blank=True)
    video = EmbedVideoField("Video")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.pk})"
