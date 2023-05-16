from datetime import datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from http import HTTPStatus
from webapp.models import Group, Client, Coach
from webapp.forms import GroupForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class GroupTest(TestCase):
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
            phone='996555555777',
            first_name='test_data',
            last_name='test_data',
            email='test@data.com',
            region='test_data',
            comment='test_data'
        )

        self.coach1 = Coach.objects.create(
            telegram_id='coach1',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test@data.com',
            started_to_work=(datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
            description='test_data',
            )

        self.group1 = Group.objects.create(
            name='Gym',
            start_at='18:00',
            coach=self.coach1
        )

        self.group2 = Group.objects.create(
            name='UFC',
            start_at='19:00',
            coach=self.coach1
        )

    def test_group_create(self):
        data = {
            'name': 'Dancing',
            'start_at': '19:00',
            'coach': self.coach1.pk
        }

        url = reverse('webapp:group_create')
        response = self.client.post(url, data=data)
        group_form = GroupForm(data=data)
        self.assertTrue(group_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Group.objects.count(), 3)

    def test_group_client_update(self):
        url = reverse('webapp:group_client_update', kwargs={'pk': self.group.pk})
        response = self.client.post(url, data={'active_client_id': [self.client1.id, self.client2.id]})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('webapp:group_detail', kwargs={'pk': self.group.pk}))

        self.client1.refresh_from_db()
        self.assertEqual(self.client1.group, self.group)

        self.client2.refresh_from_db()
        self.assertEqual(self.client2.group, self.group)

    def test_group_client_update(self):
        data = {
            'active_client_id': self.client2.pk
        }
        url = reverse('webapp:group_client_update', kwargs={'pk': self.group1.pk})
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.client2.refresh_from_db()
        self.assertEqual(self.client2.group.pk, self.group1.pk)

    def test_group_list(self):
        url = reverse('webapp:group_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_detail(self):
        url = reverse('webapp:group_detail', kwargs={'pk': self.group1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_delete(self):
        url = reverse('webapp:group_delete', kwargs={'pk': self.group1.pk})
        response = self.client.post(url)
        self.group1.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(self.group1.is_active)

    def test_group_client_delete(self):
        self.client1.group = self.group1
        self.client1.save()
        url = reverse('webapp:group_client_delete', kwargs={'pk': self.client1.pk})
        response = self.client.get(url)
        self.client1.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(self.client1.group)
