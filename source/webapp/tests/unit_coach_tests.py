from datetime import datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from http import HTTPStatus
from webapp.models import Coach
from webapp.forms import CoachForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class CoachTest(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user1 = User.objects.create_user('user1', password='password1')
        self.user1.groups.create(name='manager')
        owner_permissions = Permission.objects.filter(codename='owner', content_type__app_label='webapp')
        manager_permissions = Permission.objects.filter(codename='manager', content_type__app_label='webapp')
        all_permissions = owner_permissions.union(manager_permissions)
        self.user1.user_permissions.add(*all_permissions)
        self.client.force_login(self.user1)

        self.coach1 = Coach.objects.create(
            telegram_id='coach1',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test@data.com',
            started_to_work=(datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
            description='test_data',
            )

        self.coach2 = Coach.objects.create(
            telegram_id='coach2',
            phone='test_data',
            first_name='test_data',
            last_name='test_data',
            email='test@data.com',
            started_to_work=(datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
            description='test_data',
        )

    def test_coach_create(self):
        data1 = {
            "telegram_id": 'new_coach1',
            "phone": 'test_data',
            "first_name": 'test_data',
            "last_name": 'test_data',
            "email": 'test@data.com',
            "started_to_work": (datetime.now()).strftime('%Y-%m-%d'),
            "description": 'test_data',
        }

        data2 = {
            "telegram_id": 'new_coach2',
            "phone": 'test_data',
            "first_name": 'test_data',
            "last_name": 'test_data',
            "email": 'test@data.com',
            "started_to_work": (datetime.now()).strftime('%Y-%m-%d'),
            "description": 'test_data',
        }

        url = reverse('webapp:coach_create')
        response = self.client.post(url, data=data1)
        coach_form = CoachForm(data=data2)
        self.assertTrue(coach_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Coach.objects.count(), 3)

    def test_coach_no_telegram_id_create(self):
        data = {
            "telegram_id": 'coach3',
            "phone": 'test_data',
            "first_name": 'test_data',
            "last_name": 'test_data',
            "email": 'test@data.com',
            "started_to_work": '',
            "description": 'test_data',
        }

        url = reverse('webapp:coach_create')
        response = self.client.post(url, data=data)
        coach_form = CoachForm(data=data)
        self.assertFalse(coach_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coach_no_start_date_create(self):
        data = {
            "telegram_id": '',
            "phone": 'test_data',
            "first_name": 'test_data',
            "last_name": 'test_data',
            "email": 'test@data.com',
            "started_to_work": (datetime.now()).strftime('%Y-%m-%d'),
            "description": 'test_data',
        }

        url = reverse('webapp:coach_create')
        response = self.client.post(url, data=data)
        coach_form = CoachForm(data=data)
        self.assertFalse(coach_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coach_update(self):
        data1 = {
            "telegram_id": 'updated_coach1',
            "phone": 'updated_data',
            "first_name": 'updated_data',
            "last_name": 'updated_data',
            "email": 'updated@data.com',
            "started_to_work": (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d'),
            "description": 'updated_data',
        }

        data2 = {
            "telegram_id": 'updated_coach2',
            "phone": 'updated_data',
            "first_name": 'updated_data',
            "last_name": 'updated_data',
            "email": 'updated@data.com',
            "started_to_work": (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d'),
            "description": 'updated_data',
        }

        url = reverse('webapp:coach_update', kwargs={'pk': self.coach1.pk})
        response = self.client.post(url, data=data1)
        coach_form = CoachForm(data=data2)
        self.assertTrue(coach_form.is_valid())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.coach1.refresh_from_db()
        self.assertEqual(self.coach1.last_name, 'updated_data')

    def test_coach_list(self):
        url = reverse('webapp:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coach_detail(self):
        url = reverse('webapp:coach_detail', kwargs={'pk': self.coach1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coach_delete(self):
        url = reverse('webapp:coach_delete', kwargs={'pk': self.coach1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Coach.objects.filter(pk=self.coach1.pk).exists())
