from django.contrib.auth.models import User
from django.forms import ModelForm


class UserRegistrationForm(ModelForm):
    """Form to handle the user registration view."""

    class Meta:
        model = User
        fields = ["username", "email", "password"]
