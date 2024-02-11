from django.conf.urls import include
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("authentication.urls")),
    path("api/", include("core.urls")),
    path("api/", include("homes.urls")),
    path("api/", include("shops.urls")),
    path("api/", include("purchases.urls")),
    path("api/", include("integrations.get_receipts.urls"))
]
