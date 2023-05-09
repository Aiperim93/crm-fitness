import os
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from webapp.models import Client, Group, Training, GroupTraining, Coach, Payment
from api_v1.serializers import TrainingSerializer, GroupTrainingSerializer


class TrainingCreateAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.group = Group.objects.create(name='Test Group', start_at=datetime.now().time())
        self.client1 = Client.objects.create(telegram_id='client1', group=self.group)
        self.payment = Payment.objects.create(client=self.client1, amount=1200, paid_at=datetime.now(),
                                              payment_start_date=datetime.now(),
                                              payment_end_date=datetime.now() + timedelta(days=30))
        self.client2 = Client.objects.create(telegram_id='client2', group=self.group)
        self.url = reverse('api_v1:training_create')
        self.token = os.environ.get('API_TOKEN')

    def test_create_training(self) -> None:
        data: dict = {'telegram_id': 'client1'}
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Training.objects.count(), 1)
        self.assertEqual(Training.objects.first().client, self.client1)

    def test_create_training_invalid_client(self) -> None:
        data: dict = {'telegram_id': 'kek'}
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Training.objects.count(), 0)

    def test_create_training_inactive_client(self) -> None:
        data: dict = {'telegram_id': 'client2'}
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Training.objects.count(), 0)

    def test_create_training_missing_telegram_id(self) -> None:
        data: dict = {}
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Training.objects.count(), 0)

    def test_create_training_serializer(self) -> None:
        data: dict = {'telegram_id': 'client1'}
        serializer = TrainingSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        training = serializer.save()
        self.assertEqual(Training.objects.count(), 1)
        self.assertEqual(training.client, self.client1)


class GroupTrainingCreateAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.group = Group.objects.create(name='Test Group', start_at=datetime.now().time())
        self.coach = Coach.objects.create(telegram_id='coach1', first_name='coach1', started_to_work=datetime.now())
        self.url = reverse('api_v1:group_training_create')
        self.token = os.environ.get('API_TOKEN')

    def test_create_group_training(self) -> None:
        data = {'group': self.group.pk, 'coach': self.coach.pk}
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GroupTraining.objects.count(), 1)

    def test_create_group_training_invalid_group(self) -> None:
        data = {'group': 2, 'coach': self.coach}
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(GroupTraining.objects.count(), 0)

    def test_create_group_training_invalid_coach(self) -> None:
        data = {'group': self.group, 'coach': 1}
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(GroupTraining.objects.count(), 0)
