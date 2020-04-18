import django_filters

from core.models import *


class PostFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ('latest', 'Latest First'),
        ('oldest', 'Oldest First'),
    )

    sort_by = django_filters.ChoiceFilter(label='Sort By', choices=SORT_CHOICES, method='sort')

    class Meta:
        model = Post
        fields = ['category', 'sub_category']
    
    def sort(self, queryset, name, value):
        exp = 'created' if value == 'oldest' else '-created'
        return queryset.order_by(exp)
