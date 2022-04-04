from django.urls import path

from .api.views import HomeListView
from .api.views import HomeDetailView
from .api.views import RoomListView
from .api.views import RoomDetailView


urlpatterns = [
    path("homes/home/", HomeListView.as_view()),
    path("homes/home/<int:pk>", HomeDetailView.as_view()),
    path("homes/room/", RoomListView.as_view()),
    path("homes/room/<int:pk>", RoomDetailView.as_view()),
]
