from django.db import DEFAULT_DB_ALIAS


class AppDBRouter(object):
    """
    Router for routing the model actions to the necessary databases.

    Works based on two ways:
        1. Uses the `use_db` value set on the model layer.
        2. The `use_db` value set on the local thread.
    """

    def get_db_name(self, model, **kwargs):
        """Common function to return the db name."""

        # TODO: get from local thread
        return getattr(model, "use_db", DEFAULT_DB_ALIAS)

    def db_for_read(self, model, **hints):
        """For read actions."""

        return self.get_db_name(model, **hints)

    def db_for_write(self, model, **hints):
        """For write actions."""

        return self.get_db_name(model, **hints)
