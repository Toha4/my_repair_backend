from django.contrib import admin

from .models import CashCheck
from .models import Position


class CashСheckAdmin(admin.ModelAdmin):
    list_display = ("shop", "date", "user")
    search_fields = ("shop", "user__username")


class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "cash_check", "user")
    search_fields = ("name", "cash_check__pk", "home__user__username")


admin.site.register(CashCheck, CashСheckAdmin)
admin.site.register(Position, PositionAdmin)
