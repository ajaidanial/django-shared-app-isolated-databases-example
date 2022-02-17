from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Base URL's
# ------------------------------------------------------------------------------
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main_app.urls")),
]

# Static & Media Files
# ------------------------------------------------------------------------------
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
