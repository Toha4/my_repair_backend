from django.db.models import Model
from django.db.models.query import QuerySet

from rest_framework.request import Request

from authentication.utils import get_current_user


def get_queryset_data_user(model: Model, request: Request) -> QuerySet:
    user = get_current_user(request)
    if user:
        return model.objects.filter(user=user)
    return model.objects.none()
