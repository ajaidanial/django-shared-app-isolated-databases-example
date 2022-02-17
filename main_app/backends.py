from django.contrib.auth.backends import ModelBackend
from django.utils.connection import ConnectionDoesNotExist

from main_app.models import AppUser, UserDatabaseTracker


class AppModelBackend(ModelBackend):
    """
    Custom auth backend to authenticate the user based on the user's database.

    The default auth backend will not work since the user's data is present
    in multiple databases. Get the database based on routing tracker.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Handle when called."""

        database_tracker = UserDatabaseTracker.objects.get_or_none(
            user_identifier=username
        )

        if database_tracker:

            try:
                user = AppUser.objects.using(database_tracker.db).get_or_none(
                    username=username
                )
            except ConnectionDoesNotExist:
                user = None

            if (
                user
                and user.check_password(password)
                and self.user_can_authenticate(user)
            ):
                return user  # all good

        return None
