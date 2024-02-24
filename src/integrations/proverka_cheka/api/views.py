from django.http import Http404

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.utils import get_current_user
from integrations.proverka_cheka.api.serializers import ProverkaChekaIntegrationViewSerializer
from integrations.proverka_cheka.models import ProverkaChekaIntegration
from integrations.proverka_cheka.utils.proverka_cheka import ProverkaCheka


class ProverkaChekaIntegrationView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProverkaChekaIntegrationViewSerializer

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


class ReceiptsDataView(APIView):
    """Получить данные чека по строке qr-кода"""

    def get(self, request, *args, **kwargs):
        user = get_current_user(self.request)
        proverka_cheka_integration = ProverkaChekaIntegration.objects.filter(user=user).first()

        if not proverka_cheka_integration or not proverka_cheka_integration.api_key:
            return Response(
                {"errors": "Не найдена интеграция или отсутствует API-key!"}, status=status.HTTP_400_BAD_REQUEST
            )

        qr_raw = self.request.query_params.get("qr_raw")

        proverka_ckecka = ProverkaCheka(proverka_cheka_integration.api_key)
        receipt = proverka_ckecka.get_check_qrraw(qr_raw)

        if receipt is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(receipt, status=status.HTTP_200_OK)
