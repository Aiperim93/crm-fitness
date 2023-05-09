import os
from rest_framework import permissions


class IsBot(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.headers.get('Authorization') == os.environ.get('API_TOKEN')
