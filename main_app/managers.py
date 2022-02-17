from django.contrib.auth.models import UserManager
from django.db import DEFAULT_DB_ALIAS
from django.db.models import QuerySet


class BaseObjectManagerQuerySet(QuerySet):
    """
    The main/base manager for the apps models. This is used for including common
    model filters and methods. This is used just to make things DRY.

    This can be used in both ways:
        1. Model.app_objects.custom_method()
        2. Model.app_objects.filter().custom_method()

    Reference:
    https://stackoverflow.com/questions/2163151/custom-queryset-and-manager-without-breaking-dry#answer-21757519

    Usage on the model class
        objects = BaseObjectManagerQuerySet.as_manager()
    """

    pass


class AppUserManagerQuerySet(BaseObjectManagerQuerySet, UserManager):
    """Base class."""

    def _create_user(self, username, email, password, **extra_fields):
        """Set which db the user has to be created."""

        use_db = extra_fields.pop("use_db", DEFAULT_DB_ALIAS)
        self._db = use_db

        return super()._create_user(username, email, password, **extra_fields)

    def normalize_email(cls, email):
        """Inheritance issues."""

        return UserManager.normalize_email(email=email)
