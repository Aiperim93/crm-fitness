from datetime import datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from http import HTTPStatus
from webapp.models import Client, Payment
from webapp.forms import PaymentUpdateForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class PaymentCreateTest(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user1 = User.objects.create_user('user1', password='password1')
        self.user1.groups.create(name='manager')
        owner_permissions = Permission.objects.filter(codename='owner', content_type__app_label='webapp')
        manager_permissions = Permission.objects.filter(codename='manager', content_type__app_label='webapp')
        all_permissions = owner_permissions.union(manager_permissions)
        self.user1.user_permissions.add(*all_permissions)
        self.client.force_login(self.user1)

        self.client1 = Client.objects.create(
            telegram_id='client1',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test_data',
            region='test_data',
            comment='test_data'
        )

        self.client2 = Client.objects.create(
            telegram_id='client2',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test_data',
            region='test_data',
            comment='test_data'
        )

        self.client3 = Client.objects.create(
            telegram_id='client3',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test_data',
            region='test_data',
            comment='test_data'
        )

        self.payment1 = Payment.objects.create(
            client=self.client1,
            amount=500.00,
            paid_at=datetime.now(),
            payment_start_date=datetime.now() - timedelta(days=2),
            payment_end_date=datetime.now() + timedelta(days=28)
        )

        self.payment2 = Payment.objects.create(
            client=self.client2,
            amount=1000.00,
            paid_at=datetime.now(),
            payment_start_date=datetime.now() - timedelta(days=2),
            payment_end_date=datetime.now() + timedelta(days=28)
        )

    def test_payment_create(self):
        data = {
            'amount': 2000,
            'payment_start_date': datetime.now() - timedelta(days=2),
            'payment_end_date': datetime.now() + timedelta(days=28)
        }

        url = reverse('webapp:payment_create', kwargs={'pk': self.client3.pk})
        response = self.client.post(url, data=data)
        payment_form = PaymentUpdateForm(data=data)
        self.assertTrue(payment_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Payment.objects.count(), 3)

    def test_payment_update(self):
        data = {
            'amount': 2000.00,
            'payment_start_date': '2023-05-07',
            'payment_end_date': '2023-06-07'
        }
        url = reverse('webapp:payment_update', kwargs={'pk': self.payment2.pk})
        payment_form = PaymentUpdateForm(data=data)
        self.assertTrue(payment_form.is_valid())
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.payment2.refresh_from_db()
        self.assertEqual(self.payment2.amount, 2000.00)

    def test_payment_delete(self):
        url = reverse('webapp:payment_delete', kwargs={'pk': self.payment1.pk})
        self.client.force_login(self.user1)
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Payment.objects.filter(pk=self.payment1.pk).exists())
