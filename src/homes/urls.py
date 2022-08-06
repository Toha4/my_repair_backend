from django.urls import path

from .api.views import HomeDetailView
from .api.views import HomeListView
from .api.views import RoomDetailView
from .api.views import RoomListView
from .api.views import SetCurrentHomeView

urlpatterns = [
    path("homes/home/", HomeListView.as_view()),
    path("homes/home/<int:pk>", HomeDetailView.as_view()),
    path("homes/room/", RoomListView.as_view()),
    path("homes/room/<int:pk>", RoomDetailView.as_view()),
    path("homes/set_current_home/", SetCurrentHomeView.as_view()),
]
