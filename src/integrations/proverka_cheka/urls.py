from django.urls import path

from .api.views import ProverkaChekaIntegrationView
from .api.views import ReceiptsDataView

urlpatterns = [
    path("proverka_cheka/integration/", ProverkaChekaIntegrationView.as_view()),
    path("proverka_cheka/proverka_cheka_by_qrraw/", ReceiptsDataView.as_view()),
]
