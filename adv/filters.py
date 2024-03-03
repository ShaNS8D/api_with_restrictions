from django_filters import rest_framework as filters

from adv.models import Adv


class AdvFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = filters.DateFromToRangeFilter()
    
    class Meta:
        model = Adv
        fields = ['creator', 'created_at', 'status', 'title']
