from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.contrib.auth.mixins import PermissionRequiredMixin
from webapp.models import Group, Client
from webapp.forms import GroupForm
from webapp.forms import AddClientGroup


class GroupListView(PermissionRequiredMixin, ListView):
    model = Group
    template_name: str = 'groups/group_list.html'
    context_object_name: str = 'groups'
    paginate_by: int = 5
    permission_required = 'webapp.owner' and 'webapp.manager'

    def get_queryset(self):
        return Group.objects.filter(is_active=True)


class GroupDetailView(PermissionRequiredMixin, DetailView):
    model = Group
    template_name: str = 'groups/group_detail.html'
    permission_required = 'webapp.owner' and 'webapp.manager'

    def get_context_data(self, **kwargs) -> dict:
        clients = self.get_object().clients.filter(is_active=True).annotate(visit_count=Count('trainings')).all()
        clients_in_group = True if self.get_object().clients.active_clients().filter(is_active=True,
                                                                                     group__isnull=True) else False
        form = AddClientGroup()
        return super().get_context_data(clients=clients, form=form, clients_in_group=clients_in_group, **kwargs)


class GroupCreateView(PermissionRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name: str = 'groups/group_create.html'
    permission_required = 'webapp.owner' and 'webapp.manager'

    def get_success_url(self) -> str:
        return reverse('webapp:group_detail', kwargs={'pk': self.object.pk})


class GroupUpdateView(PermissionRequiredMixin, UpdateView):
    model = Group
    template_name: str = 'groups/group_update.html'
    form_class = GroupForm
    permission_required = 'webapp.owner' and 'webapp.manager'

    def get_success_url(self) -> str:
        return reverse('webapp:group_detail', kwargs={'pk': self.object.pk})


class GroupDeleteView(PermissionRequiredMixin, DeleteView):
    model = Group
    template_name: str = 'groups/group_delete.html'
    context_object_name: str = 'group'
    success_url: str = reverse_lazy('webapp:group_list')
    permission_required = 'webapp.owner'

    def post(self, request, *args, **kwargs):
        group = get_object_or_404(Group, pk=int(kwargs.get('pk')))
        group.is_active = False
        clients = Client.objects.all().filter(group__id=group.pk)
        for client in clients:
            client.group = None
            client.save()

        group.save()
        return redirect(self.success_url)


class GroupClientUpdateView(PermissionRequiredMixin, View):
    permission_required = 'webapp.owner' and 'webapp.manager'
    def post(self, request, *args, **kwargs):
        group_pk = kwargs.get('pk')
        client_ids = request.POST.getlist('active_client_id')
        for client_id in client_ids:
            client = get_object_or_404(Client, pk=int(client_id))
            client.group_id = group_pk
            client.save()
        return redirect(self.get_redirect_url(group_pk))

    def get_redirect_url(self, group_pk: int) -> str:
        return reverse('webapp:group_detail', kwargs={'pk': group_pk})


class GroupClientDeleteView(PermissionRequiredMixin, View):
    permission_required = 'webapp.owner' and 'webapp.manager'
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict):
        client_id = kwargs.get('pk')
        client = get_object_or_404(Client, pk=client_id)
        group_pk = client.group_id
        client.group_id = None
        client.save()
        return redirect(self.get_redirect_url(group_pk))

    def get_redirect_url(self, group_pk) -> str:
        return reverse('webapp:group_detail', kwargs={'pk': group_pk})
