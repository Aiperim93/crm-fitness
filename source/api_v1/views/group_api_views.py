from rest_framework.generics import ListAPIView
from api_v1.serializers import GroupSerializer
from webapp.models import Group
from api_v1.permissions import IsBot


class GroupListAPIView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.filter(is_active=True)
    permission_classes = [IsBot]

    def get_queryset(self):
        groups = Group.objects.filter(is_active=True)
        is_empty = self.request.query_params.get('is_empty', '')
        if is_empty.lower() == 'true':
            groups = groups.filter(clients__isnull=True)
        elif is_empty.lower() == 'false':
            groups = groups.filter(clients__isnull=False)
        return groups.distinct()
