from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.core.management import call_command
from django.urls import include, path

from main_app import helpers

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

# Apply all the necessary init app configurations
# ------------------------------------------------------------------------------
if helpers.is_default_database_synchronized():
    from main_app.models import UserDatabaseTracker

    for tracker in UserDatabaseTracker.objects.all():
        db_name = tracker.database_name
        settings.DATABASES[db_name] = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": settings.BASE_DIR / f"{db_name}.sqlite3",
        }
        call_command("migrate", database=db_name)
