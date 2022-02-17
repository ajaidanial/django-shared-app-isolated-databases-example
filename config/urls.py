from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from main_app import helpers

# app base urls
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main_app.urls")),
]

# static & media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# apply all the necessary init app configurations | called once after app init
if helpers.is_default_database_synchronized():
    from main_app.models import UserDatabaseTracker

    for tracker in UserDatabaseTracker.objects.all():
        # for each routing information
        tracker.setup_database_and_configurations()
