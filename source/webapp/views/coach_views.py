from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.db.models import Count, QuerySet
from django.contrib.auth.mixins import PermissionRequiredMixin
from webapp.models import Coach
from webapp.forms import CoachForm, CoachStatisticsPeriodForm


class CoachListView(PermissionRequiredMixin, ListView):
    model = Coach
    template_name: str = 'coaches/coach_list.html'
    context_object_name: str = 'coaches'
    paginate_by: int = 10
    permission_required = 'webapp.owner' and 'webapp.manager'


class CoachDetailView(PermissionRequiredMixin, DetailView):
    model = Coach
    template_name: str = 'coaches/coach_detail.html'
    context_object_name: str = 'coach'
    permission_required = 'webapp.owner' and 'webapp.manager'

    def get_context_data(self, **kwargs) -> dict:
        groups = self.get_object().groups.filter(is_active=True).all()
        return super().get_context_data(groups=groups, **kwargs)


class CoachCreateView(PermissionRequiredMixin, CreateView):
    model = Coach
    template_name: str = 'coaches/coach_create.html'
    form_class = CoachForm
    permission_required = 'webapp.owner' and 'webapp.manager'

    def get_success_url(self) -> str:
        return reverse('webapp:coach_detail', kwargs={'pk': self.object.pk})


class CoachUpdateView(PermissionRequiredMixin, UpdateView):
    model = Coach
    template_name: str = 'coaches/coach_update.html'
    form_class = CoachForm
    permission_required = 'webapp.owner' and 'webapp.manager'

    def get_success_url(self) -> str:
        return reverse('webapp:coach_detail', kwargs={'pk': self.object.pk})


class CoachDeleteView(PermissionRequiredMixin, DeleteView):
    model = Coach
    template_name: str = 'coaches/coach_delete.html'
    context_object_name: str = 'coach'
    success_url: str = reverse_lazy('webapp:coach_list')
    permission_required = 'webapp.owner'


class CoachStatisticsView(PermissionRequiredMixin, ListView):
    model = Coach
    template_name: str = 'coaches/coach_statistics.html'
    context_object_name: str = 'coaches'
    paginate_by: int = 10
    permission_required = 'webapp.owner' and 'webapp.manager'

    def get_queryset(self) -> QuerySet:
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        coaches = super().get_queryset()
        if start_date and end_date:
            coaches = coaches.filter(
                coach_trainings__created_at__gte=start_date, coach_trainings__created_at__lte=end_date
            )
        queryset = coaches.annotate(quantity=Count('coach_trainings')).order_by('telegram_id')
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['form'] = CoachStatisticsPeriodForm(self.request.GET)
        return context
