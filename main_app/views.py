from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from main_app.forms import UserRegistrationForm
from main_app.models import UserDatabaseTracker


def ping_view(request):
    """Just a ping view."""

    return HttpResponse("Pong!")


class UserLoginView(LoginView):
    """App view for handling login."""

    success_url = reverse_lazy("ping_view")
    template_name = "user_login_form.html"


class UserRegistrationView(FormView):
    """
    View to handle user registration. The database will be created
    and other handling are also done here.
    """

    form_class = UserRegistrationForm
    template_name = "user_registration_form.html"
    success_url = reverse_lazy("login_view")

    def form_valid(self, form):
        """Database has to be created."""

        database_name = form.cleaned_data["username"]
        user_identifier = form.cleaned_data["email"]

        # create and handle the database
        UserDatabaseTracker.objects.create(
            user_identifier=user_identifier, database_name=database_name
        ).set_up_database_and_configurations()

        # create the user on the user's database
        get_user_model().objects.create_user(**form.cleaned_data, use_db=database_name)

        return super(UserRegistrationView, self).form_valid(form=form)
