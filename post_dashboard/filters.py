import django_filters
from django.db.models import Q
from datetime import date
from core.models import *


class SearchFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value:
            return qs.filter(Q(title__icontains=value) | Q(tags__icontains=value) | Q(category__name__icontains=value) | Q(sub_category__name__icontains=value) | Q(user__company_name__icontains=value))
        else:
            return qs


class PostFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ('-created', 'Recently Uploaded'),
        ('created', 'Oldest First'),
        ('title', 'Title (A-Z)'),
        ('-title', 'Title (Z-A)'),
        ('date', 'Upclose'),
        ('-date', 'Later Future'),
        ('past', 'Past Webinars (ASC)'),
        ('-past', 'Past Webinars (DEC)'),
    )
    search = SearchFilter(label='Search')
    sort_by = django_filters.ChoiceFilter(label='Sort By', choices=SORT_CHOICES, method='sort')

    class Meta:
        model = Post
        fields = ['category', 'sub_category']

    def sort(self, queryset, name, value):
        # exp = 'created' if value == 'oldest' else '-created'
        # if value == 'oldest':
        #     exp = 'created'
        # elif value == 'asc':
        #     exp == 'title'
        # elif value == 'dec':
        #     exp == '-title'
        # else:
        #     exp = '-created'
        filter_data = {}
        if value in ['date', '-date']:
            filter_data['date__gte'] = date.today()
        elif value in ['past', '-past']:
            filter_data['date__lt'] = date.today()
            if value == 'past':
                value = 'date'
            else:
                value = '-date'
        return queryset.filter(**filter_data).order_by(value)
