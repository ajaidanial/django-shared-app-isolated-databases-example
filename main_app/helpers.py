from django.contrib.auth import login
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor

from main_app.middlewares import set_db_for_router


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
    Central app function to login a user. Handles all the
    dynamic database logic and handling.
    """

    set_db_for_router(user.db)  # needed for login
    login(request, user)
