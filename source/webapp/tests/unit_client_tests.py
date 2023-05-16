from datetime import datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from http import HTTPStatus
from webapp.models import Client, Group
from webapp.forms import ClientForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class ClientTest(TestCase):
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
            email='test@data.kg',
            region='test_data',
            comment='test_data'
        )

        self.client2 = Client.objects.create(
            telegram_id='client2',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test@data.kg',
            region='test_data',
            comment='test_data'
        )

        self.group1 = Group.objects.create(
            name='Gym',
            start_at='18:00'
        )

    def test_client_create(self):
        data1 = {
            'telegram_id': 'new_client1',
            'phone': 'test_data',
            'first_name': 'test_data',
            'last_name': 'test_data',
            'email': 'test@data.com',
            'region': 'test_data',
            'comment': 'test_data'
        }

        data2 = {
            'telegram_id': 'new_client2',
            'phone': 'test_data',
            'first_name': 'test_data',
            'last_name': 'test_data',
            'email': 'test@data.com',
            'region': 'test_data',
            'comment': 'test_data'
        }

        url = reverse('webapp:client_create')
        response = self.client.post(url, data=data1)
        client_form = ClientForm(data=data2)
        self.assertTrue(client_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Client.objects.count(), 3)

    def test_client_form_invalid_create(self):
        data = {
            'phone': 'test_data',
            'first_name': 'test_data',
            'last_name': 'test_data',
            'email': 'test@data.com',
            'region': 'test_data',
            'comment': 'test_data'
        }

        url = reverse('webapp:client_create')
        response = self.client.post(url, data=data)
        client_form = ClientForm(data=data)
        self.assertFalse(client_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_client_update(self):
        data1 = {
            'telegram_id': 'updated_client1',
            'phone': 'test_data',
            'first_name': 'test_data',
            'last_name': 'updated_client1',
            'email': 'test@data.com',
            'region': 'test_data',
            'comment': 'test_data'
        }

        data2 = {
            'telegram_id': 'updated_client2',
            'phone': 'test_data',
            'first_name': 'test_data',
            'last_name': 'test_data',
            'email': 'test@data.com',
            'region': 'test_data',
            'comment': 'test_data'
        }

        url = reverse('webapp:client_update', kwargs={'pk': self.client1.pk})
        response = self.client.post(url, data=data1)
        client_form = ClientForm(data=data2)
        self.assertTrue(client_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.client1.refresh_from_db()
        self.assertEqual(self.client1.last_name, 'updated_client1')

    def test_client_list(self):
        url = reverse('webapp:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_client_detail(self):
        url = reverse('webapp:client_detail', kwargs={'pk': self.client1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_client_delete(self):
        url = reverse('webapp:client_delete', kwargs={'pk': self.client1.pk})
        response = self.client.post(url)
        self.client1.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(self.client1.is_active)
