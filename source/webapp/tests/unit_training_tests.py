from datetime import datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from http import HTTPStatus
from webapp.models import Client, Training, Group
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class TrainingTest(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user1 = User.objects.create_user('user1', password='password1')
        self.user1.groups.create(name='manager')
        owner_permissions = Permission.objects.filter(codename='owner', content_type__app_label='webapp')
        manager_permissions = Permission.objects.filter(codename='manager', content_type__app_label='webapp')
        all_permissions = owner_permissions.union(manager_permissions)
        self.user1.user_permissions.add(*all_permissions)

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

        self.group1 = Group.objects.create(
            name='Gym',
            start_at='18:00'
        )

        self.group2 = Group.objects.create(
            name='UFC',
            start_at='19:00'
        )

        self.training1 = Training.objects.create(
            client=self.client1,
            date='2023-03-30',
            group=self.group1
        )

        self.training2 = Training.objects.create(
            client=self.client2,
            date='2023-03-31',
            group=self.group2
        )

    def test_training_create(self):
        url = reverse('webapp:training_create', kwargs={'pk': self.client3.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Training.objects.count(), 2)

    def test_training_list(self):
        url = reverse('webapp:training_list', kwargs={'pk': self.client1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_training_delete(self):
        url = reverse('webapp:training_delete', kwargs={'pk': self.training1.pk})
        self.client.force_login(self.user1)
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Training.objects.filter(pk=self.training1.pk).exists())
