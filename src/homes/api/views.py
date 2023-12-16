from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.helpers.utils import get_queryset_by_user
from app.helpers.utils import get_queryset_by_user_current_repair_object
from app.permissions import UserObjectsPermissions
from authentication.api.serializers import UserSettingsSerializer
from authentication.models import UserSettings
from authentication.utils import get_current_user

from ..models import Building, RepairObject
from ..models import Room
from .serializer import BuildingSerializer, RepairObjectSerializer
from .serializer import RoomSerializer


class RepairObjectListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Список объектов ремонта"""

    serializer_class = RepairObjectSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = get_queryset_by_user(RepairObject, self.request)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RepairObjectDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Объект ремонта"""

    permission_classes = [UserObjectsPermissions]
    queryset = RepairObject.objects.all()
    serializer_class = RepairObjectSerializer

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


class BuildingListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Строения"""

    serializer_class = BuildingSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = get_queryset_by_user_current_repair_object(Building, self.request)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BuildingDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Строение"""

    permission_classes = [UserObjectsPermissions]
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

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
        queryset = get_queryset_by_user_current_repair_object(Room, self.request)
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


class SetCurrentRepairObjectView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        current_repair_object = request.data.get("current_repair_object", False)
        repair_object = RepairObject.objects.get(pk=current_repair_object)

        if repair_object:
            user = get_current_user(request)

            if user == repair_object.user:
                user_settings = UserSettings.objects.filter(user=user).first()
                if not user_settings:
                    user_settings = UserSettings(user=user)

                user_settings.current_repair_object = repair_object
                user_settings.save()

                return Response(UserSettingsSerializer(instance=user_settings).data, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)
