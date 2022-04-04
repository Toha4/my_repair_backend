from django.urls import path

from .api.views import CashСheckDetailView
from .api.views import CashСheckListView
from .api.views import PositionListView


urlpatterns = [
    path("purchases/cash_check/", CashСheckListView.as_view()),
    path("purchases/cash_check/<int:pk>", CashСheckDetailView.as_view()),
    path("purchases/position/", PositionListView.as_view()),
]
