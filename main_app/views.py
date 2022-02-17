from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from main_app.forms import UserRegistrationForm, DummyObjectForm
from main_app.helpers import app_login
from main_app.middlewares import get_current_db_name
from main_app.models import UserDatabaseTracker, DummyObject


class PingView(LoginRequiredMixin, CreateView):
    """Just a ping view. Used to create the dummy objects also."""

    template_name = "ping_view.html"
    form_class = DummyObjectForm
    success_url = "."

    def get_context_data(self, **kwargs):
        data = super(PingView, self).get_context_data(**kwargs)

        user = self.request.user
        message = f"""
            User: {user.email}
            <br />
            Database Name: {get_current_db_name()}
            <br />
            Database Specific Dummy Data: {[_.name for _ in DummyObject.objects.all()]}
        """

        data["message"] = message
        return data


class UserLoginView(LoginView):
    """App view for handling login."""

    success_url = reverse_lazy("ping_view")
    template_name = "user_login_form.html"

    def form_valid(self, form):
        """Login and set the db on request."""

        app_login(request=self.request, user=form.get_user())
        return HttpResponseRedirect(self.success_url)


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

        # let username be both | login happens through username
        database_name = form.cleaned_data["username"]

        # create and handle the database
        tracker = UserDatabaseTracker.objects.create(
            user_identifier=database_name, database_name=database_name
        )
        tracker.setup_database_and_configurations()

        # create the user on the user's database
        get_user_model().objects.create_user(**form.cleaned_data, use_db=tracker.db)

        return super(UserRegistrationView, self).form_valid(form=form)
