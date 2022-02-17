from django.contrib.auth import get_user_model
from django.forms import ModelForm


class AppModelForm(ModelForm):
    """Base class."""

    class Meta:
        pass


class UserRegistrationForm(AppModelForm):
    """Form to handle the user registration view."""

    class Meta(AppModelForm.Meta):
        model = get_user_model()
        fields = ["username", "email", "password"]
