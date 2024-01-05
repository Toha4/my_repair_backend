from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin

from app.helpers.database import get_period_filter_lookup
from app.helpers.utils import get_queryset_by_user
from app.permissions import UserObjectsPermissions
from authentication.utils import get_current_user

from ..models import CashCheck
from ..models import Position
from .serializer import CashCheckFullSerializer
from .serializer import CashCheckSerializer
from .serializer import PositionListSerializer


class CashCheckListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Список чеков"""

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CashCheckFullSerializer
        return CashCheckSerializer

    def get_queryset(self):
        queryset = get_queryset_by_user(CashCheck, self.request)

        repair_object = self.request.query_params.get("repair_object")
        if repair_object:
            queryset = queryset.filter(repair_object=repair_object)
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


class CashCheckDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Чек"""

    permission_classes = [UserObjectsPermissions]
    queryset = CashCheck.objects.all()
    serializer_class = CashCheckSerializer

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
    """
    Все позии по чекам


    sort by: name, cash_check__date, price
    """

    serializer_class = PositionListSerializer

    def get_queryset(self):
        queryset = get_queryset_by_user(Position, self.request)

        page_size = self.request.query_params.get("page_size")
        if page_size:
            self.pagination_class.page_size = int(page_size)

        # Отдаем позиции только для текущего объекта
        user = get_current_user(self.request)
        if user and user.settings and user.settings.current_repair_object is not None:
            queryset = queryset.filter(cash_check__repair_object=user.settings.current_repair_object)
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

        # Сортировка
        sort_field = self.request.query_params.get("sortField")
        sort_order = self.request.query_params.get("sortOrder")
        if sort_field and sort_order:
            sort_order = "-" if sort_order == "desc" else ""

            if sort_field == "date":
                sort_field = "cash_check__date"

            queryset = queryset.order_by(f"{sort_order}{sort_field}", "pk")

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
