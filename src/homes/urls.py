from django.urls import path

from .api.views import BuildingDetailView, BuildingListView, RepairObjectDetailView
from .api.views import RepairObjectListView
from .api.views import RoomDetailView
from .api.views import RoomListView
from .api.views import SetCurrentRepairObjectView

urlpatterns = [
    path("homes/repair_object/", RepairObjectListView.as_view()),
    path("homes/repair_object/<int:pk>", RepairObjectDetailView.as_view()),
    path("homes/building/", BuildingListView.as_view()),
    path("homes/building/<int:pk>", BuildingDetailView.as_view()),
    path("homes/room/", RoomListView.as_view()),
    path("homes/room/<int:pk>", RoomDetailView.as_view()),
    path("homes/set_current_repair_object/", SetCurrentRepairObjectView.as_view()),
]
