import os
from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from webapp.models import Client, Coach, Group, Payment
from api_v1.serializers import ClientSerializer


class ClientListAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api_v1:client_list')
        self.token = os.environ.get('API_TOKEN')
        self.client1 = Client.objects.create(telegram_id='Client1')
        self.payment = Payment.objects.create(client=self.client1, amount=1200, paid_at=datetime.now(),
                                              payment_start_date=datetime.now(),
                                              payment_end_date=datetime.now() + timedelta(days=30))
        self.client2 = Client.objects.create(telegram_id='Client2')

    def test_get_all_clients(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.url)
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_active_clients(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.url, {'active': 'true'})
        clients = Client.objects.active_clients()
        serializer = ClientSerializer(clients, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class ClientDetailAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client1 = Client.objects.create(telegram_id='Client1')
        self.payment = Payment.objects.create(client=self.client1, amount=1200, paid_at=datetime.now(),
                                              payment_start_date=datetime.now(),
                                              payment_end_date=datetime.now() + timedelta(days=30))
        self.client2 = Client.objects.create(telegram_id='Client2')
        self.token = os.environ.get('API_TOKEN')

    def test_get_active_client(self) -> None:
        url = reverse('api_v1:client_detail', kwargs={'pk': self.client1.pk})
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(url)
        client = Client.objects.get(pk=self.client1.pk)
        serializer = ClientSerializer(client)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_inactive_client(self) -> None:
        url = reverse('api_v1:client_detail', kwargs={'pk': self.client2.pk})
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ClientCreateAPIViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('api_v1:client_create')
        self.token = os.environ.get('API_TOKEN')
        self.client1: dict = {'telegram_id': 'Client1'}
        self.client2: dict = {'telegram_id': ''}

    def test_create_valid_client(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(self.url, data=self.client1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)
        client = Client.objects.first()
        self.assertEqual(client.telegram_id, 'Client1')

    def test_create_invalid_client(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(self.url, data=self.client2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Client.objects.count(), 0)


class CheckAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.token = os.environ.get('API_TOKEN')
        self.client1 = Client.objects.create(telegram_id='client1')
        self.coach1 = Coach.objects.create(telegram_id='coach1', started_to_work=datetime.now())

    def test_get_existing_client(self) -> None:
        url = reverse('api_v1:client_check', kwargs={'telegram_id': self.client1.telegram_id})
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'client')

    def test_get_existing_coach(self) -> None:
        url = reverse('api_v1:client_check', kwargs={'telegram_id': self.coach1.telegram_id})
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'coach')

    def test_get_non_existing_user(self) -> None:
        url = reverse('api_v1:client_check', kwargs={'telegram_id': 'unknown_user'})
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ActiveClientsInGroupAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.group = Group.objects.create(name='Group', start_at=datetime.now().time())
        self.client1 = Client.objects.create(telegram_id='client1', group=self.group)
        self.payment1 = Payment.objects.create(client=self.client1, amount=1200, paid_at=datetime.now(),
                                               payment_start_date=datetime.now(),
                                               payment_end_date=datetime.now() + timedelta(days=30))
        self.client2 = Client.objects.create(telegram_id='client2', group=self.group)
        self.payment2 = Payment.objects.create(client=self.client2, amount=1200, paid_at=datetime.now(),
                                               payment_start_date=datetime.now(),
                                               payment_end_date=datetime.now() + timedelta(days=30))
        self.client3 = Client.objects.create(telegram_id='client3', group=self.group)
        self.url = reverse('api_v1:client_in_group', kwargs={'group_id': self.group.pk})
        self.token = os.environ.get('API_TOKEN')

    @patch('webapp.manager.ActiveClientManager.active_clients')
    def test_get_active_clients_in_group(self, mock_active_clients) -> None:
        serializer = ClientSerializer([self.client1, self.client2, self.client3], many=True).data
        mock_active_clients.return_value = Client.objects.filter(pk__in=[self.client1.pk, self.client2.pk])
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.url, {'active': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer)

    def test_get_non_existing_group(self) -> None:
        url = reverse('api_v1:client_in_group', kwargs={'group_id': 9999})
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
