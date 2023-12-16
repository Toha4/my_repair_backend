from django.db.models import Model
from django.db.models.query import QuerySet

from rest_framework.request import Request

from authentication.utils import get_current_user


def get_queryset_by_user(model: Model, request: Request) -> QuerySet:
    user = get_current_user(request)
    if user:
        return model.objects.filter(user=user)
    return model.objects.none()


def get_queryset_by_user_current_repair_object(model: Model, request: Request) -> QuerySet:
    user = get_current_user(request)
    if user and user.settings and user.settings.current_repair_object is not None:
        return model.objects.filter(user=user, repair_object=user.settings.current_repair_object)
    return model.objects.none()
