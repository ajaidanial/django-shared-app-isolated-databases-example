from django.conf import settings
from django.core.management import call_command
from django.db import models, DEFAULT_DB_ALIAS


class UserDatabaseTracker(models.Model):
    """Table to track which database belongs to which user."""

    use_db = DEFAULT_DB_ALIAS

    user_identifier = models.CharField(max_length=255, unique=True)
    database_name = models.CharField(max_length=255)

    def set_up_database_and_configurations(self):
        """Adds the db to the settings and creates the db if necessary."""

        db_name = self.database_name
        settings.DATABASES[db_name] = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": settings.BASE_DIR / f"{db_name}.sqlite3",
        }
        call_command("migrate", database=db_name)
