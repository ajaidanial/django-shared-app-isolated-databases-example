from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.management import call_command
from django.db import DEFAULT_DB_ALIAS, models

from main_app.managers import AppUserManagerQuerySet, BaseObjectManagerQuerySet


class BaseModel(models.Model):
    """Base class for easy implementations."""

    class Meta:
        abstract = True

    objects = BaseObjectManagerQuerySet.as_manager()


class AppUser(AbstractUser):
    """Custom app's User model. Overridden for easy implementations."""

    objects = AppUserManagerQuerySet.as_manager()


class UserDatabaseTracker(BaseModel):
    """Table to track which database belongs to which user."""

    use_db = DEFAULT_DB_ALIAS

    user_identifier = models.CharField(max_length=255, unique=True)
    database_name = models.CharField(max_length=255)

    @property
    def db(self):
        return self.database_name

    def set_up_database_and_configurations(self):
        """Adds the db to the settings and creates the db if necessary."""

        db_name = self.database_name

        print(f"Initializing database: {db_name}")
        settings.DATABASES[db_name] = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": settings.BASE_DIR / f"{db_name}.sqlite3",
        }
        call_command("migrate", database=db_name)
