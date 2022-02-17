from django.db import connections, DEFAULT_DB_ALIAS
from django.db.migrations.executor import MigrationExecutor


def is_default_database_synchronized():
    """
    Checks if the default database is synchronized or migrated. Used
    to apply the necessary init settings.* configurations.
    """

    connection = connections[DEFAULT_DB_ALIAS]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)
