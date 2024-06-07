from django_filters import FilterSet, DateFilter, CharFilter, ChoiceFilter
from django import forms
from .models import News
from django.db.models import Q, F


def filter_not_empty(queryset, name, value):
    lookup = '__'.join([name, 'isnull'])
    return queryset.filter(**{lookup: False})


class NewsFilter(FilterSet):
    date = DateFilter(field_name="date", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),method=filter_not_empty)
    
    SORT_CHOICES = (

        ('newest', 'Newest News'),
        ('oldest', 'Oldest News'),
        ('most_viewed', 'Most Viewed News')
    )

    sort_by = ChoiceFilter(choices=SORT_CHOICES, method='custom_sort', label='Sort By')
    search = CharFilter(method='custom_search', label='Search')

    class Meta:
        model = News
        fields = {
            'news_type': ['exact'],
            'date':[],
            'user':['exact']
        }

    def custom_search(self, queryset, name, value):
        return queryset.filter(
        Q(title__icontains=value) | Q(description__icontains=value)
    )


    def custom_sort(self, queryset, name, value):
        if value == 'newest':
            return queryset.order_by('-date')
        elif value == 'oldest':
            return queryset.order_by('date')
        elif value == 'most_viewed':
            return queryset.annotate(news_view_count=F('view_count')).order_by('-news_view_count')
        return queryset
