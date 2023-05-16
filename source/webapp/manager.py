from datetime import datetime, date, timedelta
from django.db import models
from django.db.models import Max
from django.db.models import Q

class ActiveClientManager(models.Manager):
    def active_clients(self):
        now = datetime.now().date()
        return super().get_queryset().filter(
            payments__payment_end_date__gt=now
        ).exclude(
            payments__lazy_days__start_date__lte=now,
            payments__lazy_days__end_date__gte=now
        ).distinct()

    def active_payment(self, client):
        return client.payments.filter(payment_end_date__gte=date.today()).first()


    def get_queryset(self):
        return super().get_queryset().annotate(
            latest_payment=Max('payments__payment_end_date')
        )


    def inactive_clients(self):
        now = datetime.now().date()
        thirty_days_ago = now - timedelta(days=30)
        one_day_from_now = now + timedelta(days=1)
        stop_sending_message = now - timedelta(days=3)
        return self.get_queryset().filter(
            payments__created_at__gt=thirty_days_ago,
            latest_payment__lte=one_day_from_now,
            latest_payment__gt=stop_sending_message,
        ).exclude(
            payments__lazy_days__start_date__lte=now,
            payments__lazy_days__end_date__gte=now
        ).distinct()
