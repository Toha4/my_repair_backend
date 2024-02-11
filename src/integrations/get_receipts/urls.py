from django.urls import path

from .api.views import ReceiptsDataView


urlpatterns = [
    path("get_receipts/get_receipts_by_qrraw/", ReceiptsDataView.as_view()),
]