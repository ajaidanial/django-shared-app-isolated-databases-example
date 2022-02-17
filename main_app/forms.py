from django.contrib.auth import get_user_model
from django.forms import ModelForm

from main_app.models import DummyObject


class AppModelForm(ModelForm):
    """Base class. If in case need to override in the future."""

    class Meta:
        pass


class UserRegistrationForm(AppModelForm):
    """Form to handle the user registration view."""

    class Meta(AppModelForm.Meta):
        model = get_user_model()
        fields = ["username", "email", "password"]

    def clean(self):
        self._validate_unique = False
        return self.cleaned_data


class DummyObjectForm(AppModelForm):
    """Form to handle the dummy object creation."""

    class Meta(AppModelForm.Meta):
        model = DummyObject
        fields = ["name"]
