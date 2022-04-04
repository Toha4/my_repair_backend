from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin

from app.helpers.utils import get_queryset_data_user
from app.permissions import UserObjectsPermissions

from ..models import Home
from ..models import Room
from .serializer import HomeSerializer
from .serializer import RoomSerializer


class HomeListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Список домов"""

    serializer_class = HomeSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = get_queryset_data_user(Home, self.request)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class HomeDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Дом"""

    permission_classes = [UserObjectsPermissions]
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

    def get_object(self):
        pk = self.kwargs.pop("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RoomListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Список комнат"""

    serializer_class = RoomSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = get_queryset_data_user(Room, self.request)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RoomDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Комната"""

    permission_classes = [UserObjectsPermissions]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_object(self):
        pk = self.kwargs.pop("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
