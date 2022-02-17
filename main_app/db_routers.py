from django.db import DEFAULT_DB_ALIAS

from main_app.middlewares import get_current_db_name


class AppDBRouter:
    """
    Router for routing the model actions to the necessary databases.

    Works based on two ways:
        1. Uses the `use_db` value set on the model layer.
        2. The `use_db` value set on the local thread while login and request.
    """

    def get_db_name(self, model, **kwargs):
        """Common function to return the db name."""

        # first preference from the model
        use_db = getattr(model, "use_db", None)

        # second preference from the thread
        if not use_db:
            use_db = get_current_db_name()

        return use_db if use_db else DEFAULT_DB_ALIAS

    def db_for_read(self, model, **hints):
        """For read actions."""

        return self.get_db_name(model, **hints)

    def db_for_write(self, model, **hints):
        """For write actions."""

        return self.get_db_name(model, **hints)

    def allow_relation(self, *args, **kwargs):
        """Prevent unnecessary breakages."""

        return True

    def allow_syncdb(self, *args, **kwargs):
        """Prevent unnecessary breakages."""

        return None
