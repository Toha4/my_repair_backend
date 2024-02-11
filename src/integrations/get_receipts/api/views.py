from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from integrations.get_receipts.utils.proverka_checka import ProverkaChecka
from app.settings import PROVERKA_CHEKA_API_KEY



class ReceiptsDataView(APIView):
    """ Получить данные чека по строке qr-кода """

    def get(self, request, *args, **kwargs):
        qr_raw = self.request.query_params.get("qr_raw")

        # TODO: API ключ переместить в настройки интеграции
        api_key = PROVERKA_CHEKA_API_KEY
        proverka_ckecka = ProverkaChecka(api_key)
        receipt = proverka_ckecka.get_check_qrraw(qr_raw)

        if receipt is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(receipt, status=status.HTTP_200_OK)
     