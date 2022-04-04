from django.contrib import admin

from .models import Home
from .models import Room


class HomeAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__username")


class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "home", "user")
    search_fields = ("name", "home", "home__user__username")


admin.site.register(Home, HomeAdmin)
admin.site.register(Room, RoomAdmin)
