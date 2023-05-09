from django.http import HttpRequest
from django.views.generic import DetailView, View, DeleteView
from webapp.models import Training, Client
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class TrainingListView(PermissionRequiredMixin, DetailView, MultipleObjectMixin):
    model = Client
    template_name: str = 'trainings/training_list.html'
    paginate_by: int = 8
    permission_required = 'webapp.owner' and 'webapp.manager'

    def get_context_data(self, **kwargs) -> dict:
        client = get_object_or_404(Client, pk=self.kwargs.get('pk'))
        object_list = client.trainings.all()
        context = super(TrainingListView, self).get_context_data(object_list=object_list)
        return context


class TrainingCreateView(PermissionRequiredMixin, View):
    permission_required = 'webapp.owner' and 'webapp.manager'
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict):
        client = get_object_or_404(Client.objects.filter(pk=self.kwargs.get('pk'), is_active=True))
        if client in Client.objects.active_clients():
            training = Training.objects.create(client=client, group=client.group)
            training.save()
        return redirect('webapp:client_detail', client.pk)


class TrainingDeleteView(PermissionRequiredMixin, DeleteView):
    model = Training
    template_name: str = 'trainings/training_delete.html'
    context_object_name: str = 'training'
    permission_required = 'webapp.owner' and 'webapp.manager'

    def get_success_url(self) -> str:
        return reverse('webapp:training_list', kwargs={'pk': self.object.client.pk})
