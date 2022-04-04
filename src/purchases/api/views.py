from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin

from app.helpers.database import get_period_filter_lookup
from app.helpers.utils import get_queryset_data_user
from app.permissions import UserObjectsPermissions

from ..models import CashСheck
from ..models import Position
from .serializer import CashСheckFullSerializer
from .serializer import CashСheckSerializer
from .serializer import PositionListSerializer


class CashСheckListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Список чеков"""

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CashСheckFullSerializer
        return CashСheckSerializer

    def get_queryset(self):
        queryset = get_queryset_data_user(CashСheck, self.request)

        home = self.request.query_params.get("home")
        if home:
            queryset = queryset.filter(home=home)
        else:
            queryset = queryset.none()

        shop = self.request.query_params.get("shop")
        if shop:
            queryset = queryset.filter(shop=shop)

        date_begin = self.request.query_params.get("date_begin")
        date_end = self.request.query_params.get("date_end")
        if date_begin or date_end:
            queryset = queryset.filter(get_period_filter_lookup("date", date_begin, date_end))

        name = self.request.query_params.get("name")
        if name:
            # TODO: Lower не работает в SQLLITE. Проверить после перехода на другую БД.
            queryset = queryset.filter(positions__name__icontains=name.lower())

        room = self.request.query_params.get("room")
        if room:
            queryset = queryset.filter(positions__room=room)

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(positions__category=category)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CashСheckDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Чек"""

    permission_classes = [UserObjectsPermissions]
    queryset = CashСheck.objects.all()
    serializer_class = CashСheckSerializer

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


class PositionListView(ListModelMixin, GenericAPIView):
    """Все позии по чекам"""

    serializer_class = PositionListSerializer

    def get_queryset(self):
        queryset = get_queryset_data_user(Position, self.request)

        home = self.request.query_params.get("home")
        if home:
            queryset = queryset.filter(cash_check__home=home)
        else:
            queryset = queryset.none()

        shop = self.request.query_params.get("shop")
        if shop:
            queryset = queryset.filter(cash_check__shop=shop)

        date_begin = self.request.query_params.get("date_begin")
        date_end = self.request.query_params.get("date_end")
        if date_begin or date_end:
            queryset = queryset.filter(get_period_filter_lookup("cash_check__date", date_begin, date_end))

        name = self.request.query_params.get("name")
        if name:
            # TODO: Lower не работает в SQLLITE. Проверить после перехода на другую БД.
            queryset = queryset.filter(name__icontains=name.lower())

        room = self.request.query_params.get("room")
        if room:
            queryset = queryset.filter(room=room)

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
