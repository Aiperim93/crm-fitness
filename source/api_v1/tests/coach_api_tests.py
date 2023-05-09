import os
from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from webapp.models import Coach, Group
from api_v1.serializers import CoachSerializer


class GroupCoachAPITestCase(APITestCase):
    def setUp(self):
        self.token = os.environ.get('API_TOKEN')
        self.group = Group.objects.create(name='Group', start_at=datetime.now().time())
        self.coach1 = Coach.objects.create(telegram_id='coach1', first_name='coach1', started_to_work=datetime.now())
        self.coach2 = Coach.objects.create(telegram_id='coach2', first_name='coach2', started_to_work=datetime.now())
        self.group.coach = self.coach1
        self.group.save()

    def test_get_coaches(self):
        url = reverse('api_v1:coach_info', args=[self.group.id])
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['base_coach']['id'], self.coach1.id)
        self.assertEqual(len(response.data['other_coaches']), 1)
        self.assertEqual(response.data['other_coaches'][0]['id'], self.coach2.id)

    def test_get_coaches_with_nonexistent_group(self):
        url = reverse('api_v1:coach_info', args=[1000])
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_coaches_with_no_base_coach(self):
        self.group.coach = None
        self.group.save()
        url = reverse('api_v1:coach_info', args=[self.group.id])
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['base_coach'])
        self.assertEqual(len(response.data['other_coaches']), 2)
        serializer = CoachSerializer(Coach.objects.all(), many=True)
        self.assertEqual(response.data['other_coaches'], serializer.data)
