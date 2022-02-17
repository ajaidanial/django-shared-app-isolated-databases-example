from django.contrib.auth.backends import ModelBackend

from main_app.models import UserDatabaseTracker, AppUser


class AppModelBackend(ModelBackend):
    """Custom backend to authenticate the user based on the database."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Handle when called."""

        database_tracker = UserDatabaseTracker.objects.get_or_none(
            user_identifier=username
        )

        if database_tracker:
            user = AppUser.objects.using(database_tracker.db).get_or_none(
                username=username
            )

            if user.check_password(password) and self.user_can_authenticate(user):
                return user  # all good

        return super(AppModelBackend, self).authenticate(
            request=request, username=username, password=password, **kwargs
        )
