from django.urls import path

from .api.views import ProverkaChekaIntegrationView
from .api.views import ReceiptScanningDetailView
from .api.views import ReceiptScanningListView
from .api.views import ReceiptsScnningByQrView

urlpatterns = [
    path("proverka_cheka/integration/", ProverkaChekaIntegrationView.as_view()),
    path("proverka_cheka/proverka_cheka_by_qrraw/", ReceiptsScnningByQrView.as_view()),
    path("proverka_cheka/receipt_scanning/", ReceiptScanningListView.as_view()),
    path("proverka_cheka/receipt_scanning/<int:pk>", ReceiptScanningDetailView.as_view()),
]
