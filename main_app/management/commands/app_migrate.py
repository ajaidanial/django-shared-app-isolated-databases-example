from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Custom app command to apply migrations to all the databases."

    def handle(self, *args, **kwargs):
        """Call all the necessary commands."""

        database_names = settings.DATABASES.keys()
        for _ in database_names:
            self.stdout.write(f"Migrating for database: {_}")
            call_command("migrate", database=_)
            self.stdout.write("\n")
