from django.contrib.auth import login
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor


def is_default_database_synchronized():
    """
    Checks if the default database is synchronized or migrated. Used
    to apply the necessary init settings.* configurations.
    """

    try:

        connection = connections[DEFAULT_DB_ALIAS]
        connection.prepare_database()
        executor = MigrationExecutor(connection)
        targets = executor.loader.graph.leaf_nodes()
        return not executor.migration_plan(targets)

    except:  # noqa

        return False


def app_login(request, user):
    """
    Central app function to login. Handles all the
    dynamic dy logic and handling.
    """

    # TODO: implement database based logic
    breakpoint()
