from django.urls import path

from .api.views import ShopDetailView
from .api.views import ShopListView


urlpatterns = [
    path("shops/shop/", ShopListView.as_view()),
    path("shops/shop/<int:pk>", ShopDetailView.as_view()),
]
