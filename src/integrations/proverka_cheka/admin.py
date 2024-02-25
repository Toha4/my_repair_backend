from django.contrib import admin

import nested_admin

from .models import ProverkaChekaIntegration
from .models import ReceiptItem
from .models import ReceiptScanning


class ReceiptItemInline(nested_admin.NestedTabularInline):
    model = ReceiptItem
    extra = 0


class ProverkaChekaIntegrationAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)


class ReceiptScanningAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "organization",
        "user",
    )
    search_fields = (
        "date",
        "organization",
        "user__username",
    )
    readonly_fields = ("created",)
    inlines = (ReceiptItemInline,)


admin.site.register(ProverkaChekaIntegration, ProverkaChekaIntegrationAdmin)
admin.site.register(ReceiptScanning, ReceiptScanningAdmin)
