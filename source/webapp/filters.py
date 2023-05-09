import django_filters
from .models import Client
from datetime import datetime

CHOICES = (
    (0, 'All'),
    (1, 'Paid'),
    (2, 'Unpaid')
)


class ClientFilter(django_filters.FilterSet):
    is_paid = django_filters.ChoiceFilter(
        choices=CHOICES,
        label='Оплата',
        method='filter_is_paid',
        empty_label=None
    )

    class Meta:
        model = Client
        fields = ['is_paid']

    def filter_is_paid(self, queryset, name, val):
        if val == '1':
            return queryset.filter(payments__payment_start_date__lte=datetime.now(),
                                   payments__payment_end_date__gte=datetime.now())
        if val == '2':
            return queryset.exclude(payments__payment_start_date__lte=datetime.now(),
                                    payments__payment_end_date__gte=datetime.now())
        return queryset
