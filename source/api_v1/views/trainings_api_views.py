from rest_framework.generics import CreateAPIView
from api_v1.serializers import TrainingSerializer, GroupTrainingSerializer
from webapp.models import Training, GroupTraining
from api_v1.permissions import IsBot


class TrainingCreateAPIView(CreateAPIView):
    serializer_class = TrainingSerializer
    queryset = Training.objects.all()
    permission_classes = [IsBot]


class GroupTrainingCreateAPIView(CreateAPIView):
    serializer_class = GroupTrainingSerializer
    queryset = GroupTraining.objects.all()
    permission_classes = [IsBot]
