import django_filters
from django.db.models import Q

from core.models import *


class SearchFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value:
            return qs.filter(Q(title__icontains=value) | Q(tags__icontains=value) | Q(category__name__icontains=value) | Q(sub_category__name__icontains=value) | Q(user__company_name__icontains=value))
        else:
            return qs


class PostFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ('latest', 'Latest First'),
        ('oldest', 'Oldest First'),
    )
    search = SearchFilter(label='Search')
    sort_by = django_filters.ChoiceFilter(label='Sort By', choices=SORT_CHOICES, method='sort')

    class Meta:
        model = Post
        fields = ['category', 'sub_category']

    def sort(self, queryset, name, value):
        exp = 'created' if value == 'oldest' else '-created'
        return queryset.order_by(exp)
