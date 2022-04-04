from rest_framework.permissions import BasePermission

from authentication.utils import get_current_user


class UserObjectsPermissions(BasePermission):
    """Сопоставление моделей с пользователем"""

    message = "Эти данные принадлежат другому пользователю."

    def has_object_permission(self, request, view, obj):
        user = get_current_user(request)
        return obj.user == user
