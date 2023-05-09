from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from api_v1.serializers import ClientSerializer, ClientSerializerPatch
from django.http import HttpRequest, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Client, Coach, Group
from rest_framework import status
from api_v1.permissions import IsBot
from datetime import datetime
from rest_framework.permissions import IsAuthenticated


class ClientListAPIView(ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsBot]

    def get_queryset(self) -> QuerySet:
        if self.request.query_params.get('active') == 'true':
            return Client.objects.active_clients()
        else:
            return Client.objects.all()


class ClientDetailAPIView(RetrieveAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.active_clients()
    permission_classes = [IsBot]


class ClientCreateAPIView(CreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsBot]


class ClientUpdateAPIView(UpdateAPIView):
    serializer_class = ClientSerializerPatch
    queryset = Client.objects.all()
    lookup_field = 'telegram_id'
    permission_classes = [IsBot]

    def patch(self, request, telegram_id: str, *args, **kwargs):
        client = get_object_or_404(Client, telegram_id=telegram_id)
        serializer = ClientSerializerPatch(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckAPIView(APIView):
    permission_classes = [IsBot]

    def get(self, request: HttpRequest, telegram_id: str, *args: tuple, **kwargs: dict) -> Response:
        try:
            client = Client.objects.get(telegram_id=telegram_id)
            if client.is_active:
                return Response({'result': 'client'}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'client_deleted'}, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            try:
                Coach.objects.get(telegram_id=telegram_id)
                return Response({'result': 'coach'}, status=status.HTTP_200_OK)
            except Coach.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)


class ActiveClientsInGroupAPIView(ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsBot]

    def get_queryset(self) -> QuerySet:
        group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        if self.request.query_params.get('active') == 'True':
            return Client.objects.active_clients().filter(group=group)
        else:
            return Client.objects.all().filter(group=group)


class TotalActiveClientsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            date = datetime.now().date()
        else:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
        active_clients = Client.objects.filter(payments__payment_start_date__lte=date,
                                               payments__payment_end_date__gte=date, is_active=True)
        count = active_clients.count()
        return Response({'count': count})
