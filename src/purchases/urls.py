from django.urls import path

from .api.views import CashCheckDetailView
from .api.views import CashCheckListView
from .api.views import PositionListView


urlpatterns = [
    path("purchases/cash_check/", CashCheckListView.as_view()),
    path("purchases/cash_check/<int:pk>", CashCheckDetailView.as_view()),
    path("purchases/position/", PositionListView.as_view()),
]
