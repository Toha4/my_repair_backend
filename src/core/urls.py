from django.urls import path

from .api.views import CategoryListView
from .api.views import CategoryDetailView


urlpatterns = [
    path("core/category/", CategoryListView.as_view()),
    path("core/category/<int:pk>", CategoryDetailView.as_view()),
]
