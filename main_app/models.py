from django.db import models, DEFAULT_DB_ALIAS


class UserDatabaseTracker(models.Model):
    """Table to track which database belongs to which user."""

    use_db = DEFAULT_DB_ALIAS

    user_identifier = models.CharField(max_length=255, unique=True)
    database_name = models.CharField(max_length=255)
