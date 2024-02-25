from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.helpers.utils import get_queryset_by_user
from app.permissions import UserObjectsPermissions
from authentication.utils import get_current_user
from integrations.proverka_cheka.api.serializers import ProverkaChekaIntegrationSerializer
from integrations.proverka_cheka.api.serializers import ReceiptScanningDetailSerializer
from integrations.proverka_cheka.api.serializers import ReceiptScanningListSerializer
from integrations.proverka_cheka.models import ProverkaChekaIntegration
from integrations.proverka_cheka.models import ReceiptScanning
from integrations.proverka_cheka.utils.proverka_cheka import ProverkaCheka


class ProverkaChekaIntegrationView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProverkaChekaIntegrationSerializer

    def get_object(self):
        user = get_current_user(self.request)

        if not user:
            raise Http404

        proverka_cheka_integration = ProverkaChekaIntegration.objects.filter(user=user).first()

        # Если экземпляра интеграции нет, то создаем его
        if not proverka_cheka_integration:
            proverka_cheka_integration = ProverkaChekaIntegration(user=user)
            proverka_cheka_integration.save()

        return proverka_cheka_integration

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ReceiptsScnningByQrView(APIView):
    """Получить данные чека по строке qr-кода"""

    def get(self, request, *args, **kwargs):
        user = get_current_user(self.request)
        proverka_cheka_integration = ProverkaChekaIntegration.objects.filter(user=user).first()

        if not proverka_cheka_integration or not proverka_cheka_integration.api_key:
            return Response(
                {"errors": "Не найдена интеграция или отсутствует API-key!"}, status=status.HTTP_400_BAD_REQUEST
            )

        qr_raw = self.request.query_params.get("qr_raw")

        # Если ранее загружали, то отдаем его
        receipt_scanning = ReceiptScanning.objects.filter(qr_raw=qr_raw).first()
        if receipt_scanning:
            return Response(ReceiptScanningDetailSerializer(receipt_scanning).data, status=status.HTTP_200_OK)

        proverka_ckecka = ProverkaCheka(proverka_cheka_integration.api_key)
        receipt = proverka_ckecka.get_check_qrraw(qr_raw)
        if receipt is None:
            return Response({"errors": "Не удалось получить данные"}, status=status.HTTP_400_BAD_REQUEST)

        # Сохраняем данные
        serializer = ReceiptScanningDetailSerializer(data=receipt)
        serializer.context["request"] = self.request
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReceiptScanningListView(ListModelMixin, GenericAPIView):
    """
    Все отсканированные чеки

    general_search: organization, item_name
    filter: is_added_check
    """

    serializer_class = ReceiptScanningListSerializer

    def get_queryset(self):
        queryset = get_queryset_by_user(ReceiptScanning, self.request)

        page_size = self.request.query_params.get("page_size")
        if page_size:
            self.pagination_class.page_size = int(page_size)

        general_search = self.request.query_params.get("general_search")
        if general_search:
            queryset = queryset.filter(
                Q(organization__icontains=general_search.lower()) | Q(items__name__icontains=general_search.lower())
            ).distinct()

        is_added_check = self.request.query_params.get("is_added_check")
        if is_added_check:
            # TODO: Добавить фильтр по добавленному чеку
            pass

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ReceiptScanningDetailView(RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """Отсканированный чек"""

    permission_classes = [UserObjectsPermissions]
    serializer_class = ReceiptScanningDetailSerializer
    queryset = ReceiptScanning.objects.all()

    def get_object(self):
        pk = self.kwargs.pop("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
