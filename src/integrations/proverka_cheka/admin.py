from django.contrib import admin

from .models import ProverkaChekaIntegration


class ProverkaChekaIntegrationAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)


admin.site.register(ProverkaChekaIntegration, ProverkaChekaIntegrationAdmin)
