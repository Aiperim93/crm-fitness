from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin

class StatisticsView(PermissionRequiredMixin, TemplateView):
    template_name = 'stats/stats.html'
    permission_required = 'webapp.owner' and 'webapp.manager'
