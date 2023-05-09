from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from webapp.models import Client, Group, Training, Coach, GroupTraining
from django.core.validators import RegexValidator


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['telegram_id']


class ClientSerializerPatch(serializers.ModelSerializer):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed.")

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone', 'region', 'photo']

    def validate_phone(self, value):
        self.phone_regex(value)
        return value


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class TrainingSerializer(serializers.ModelSerializer):
    telegram_id: str = serializers.CharField()

    class Meta:
        model = Training
        fields = ['telegram_id']

    def save(self, **kwargs) -> Training:
        telegram_id: str = self.validated_data['telegram_id']
        client = get_object_or_404(Client, telegram_id=telegram_id)
        if client.is_active and client in Client.objects.active_clients():
            group = client.group
            training = Training.objects.create(client=client, group=group)
            training.save()
            return training
        raise ValidationError("The client is inactive.")


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ['id', 'first_name', 'last_name']


class GroupTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupTraining
        fields = '__all__'
