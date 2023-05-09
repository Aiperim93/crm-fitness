from django.http import HttpRequest
from rest_framework.response import Response
from api_v1.serializers import CoachSerializer
from rest_framework.views import APIView
from webapp.models import Coach, Group
from api_v1.permissions import IsBot


class CoachInfoAPIView(APIView):
    permission_classes = [IsBot]

    def get(self, request: HttpRequest, group_id: int, *args: tuple, **kwargs: dict) -> Response:
        try:
            group = Group.objects.get(id=group_id)
            base_coach_id = group.coach.id
            queryset = Coach.objects.exclude(id=base_coach_id)
            serializer = CoachSerializer(queryset, many=True)
            coaches_info = {
                "base_coach": CoachSerializer(Coach.objects.get(id=base_coach_id)).data,
                "other_coaches": serializer.data
            }
            return Response(coaches_info)
        except Group.DoesNotExist:
            return Response({"error": "Group does not exist."}, status=404)
        except AttributeError:
            base_coach_id = None
            queryset = Coach.objects.all()
            serializer = CoachSerializer(queryset, many=True)
            coaches_info = {
                "base_coach": base_coach_id,
                "other_coaches": serializer.data
            }
            return Response(coaches_info)
