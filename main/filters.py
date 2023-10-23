import django_filters

from main.models import Payment


class PaymentFilter(django_filters.FilterSet):
    course = django_filters.CharFilter(field_name='course__name', lookup_expr='iexact')
    lesson = django_filters.CharFilter(field_name='lesson__name', lookup_expr='iexact')
    method = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'method']



