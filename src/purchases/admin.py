from django.contrib import admin

from .models import CashCheck
from .models import Position


class CashCheckAdmin(admin.ModelAdmin):
    list_display = ("shop", "date", "user")
    search_fields = ("shop", "user__username")


class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "cash_check", "user")
    search_fields = ("name", "cash_check__pk", "repair_object__user__username")


admin.site.register(CashCheck, CashCheckAdmin)
admin.site.register(Position, PositionAdmin)
