from django_filters import rest_framework as filters
from Transaction.models import Add_Transaction


class Filter(filters.FilterSet):
    year = filters.NumberFilter(field_name='created_at', lookup_expr='year')
    month = filters.NumberFilter(field_name='created_at', lookup_expr='month')
    type = filters.CharFilter(field_name='type')
    start_date = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Add_Transaction
        fields = ['year', 'month', 'type', 'start_date', 'end_date']