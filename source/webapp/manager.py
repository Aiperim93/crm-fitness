from datetime import datetime, date
from django.db import models


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
