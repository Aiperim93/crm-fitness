from datetime import datetime, timedelta
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.mixins import PermissionRequiredMixin
from webapp.models import Client, Payment
from webapp.forms import PaymentForm, PaymentUpdateForm


class PaymentCreateView(PermissionRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name: str = 'payments/payment_create.html'
    permission_required = 'webapp.owner' and 'webapp.manager'

    def form_valid(self, form):
        client = get_object_or_404(Client, pk=self.kwargs.get('pk'))
        if not client.is_active:
            return HttpResponseBadRequest('Cannot create payment for deleted client.')
        form.instance.client = client
        if client.payments.exists():
            latest_payment = client.payments.latest('payment_end_date')
            payment_start_date = latest_payment.payment_end_date + timedelta()
        else:
            payment_start_date = datetime.now()
        payment_end_date = payment_start_date + timedelta(days=30)
        form.instance.payment_start_date = payment_start_date
        form.instance.payment_end_date = payment_end_date
        response = super().form_valid(form)
        client.save()
        return response

    def get_success_url(self):
        return reverse('webapp:client_detail', kwargs={'pk': self.object.client.pk})


class PaymentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Payment
    template_name: str = 'payments/payment_update.html'
    form_class = PaymentUpdateForm
    permission_required = 'webapp.owner' and 'webapp.manager'

    def get_success_url(self) -> str:
        return reverse('webapp:client_detail', kwargs={'pk': self.object.client.pk})


class PaymentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Payment
    template_name = 'payments/payment_delete.html'
    permission_required = 'webapp.owner'

    def form_valid(self, form):
        success_url = self.get_success_url()
        payment = self.get_object()
        client = payment.client
        client.save()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self) -> str:
        return reverse('webapp:client_detail', kwargs={'pk': self.object.client.pk})
