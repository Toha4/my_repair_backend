from django.contrib import admin

from .models import Building, RepairObject
from .models import Room


class RepairObjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__username")


class BuildingAdmin(admin.ModelAdmin):
    list_display = ("name", "repair_object", "user")
    search_fields = ("name", "repair_object", "repair_object__user__username")


class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "repair_object", "building", "user")
    search_fields = ("name", "repair_object", "building", "repair_object__user__username")


admin.site.register(RepairObject, RepairObjectAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Room, RoomAdmin)
