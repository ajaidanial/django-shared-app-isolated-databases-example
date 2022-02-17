from django.conf import settings
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.connection import ConnectionDoesNotExist
from django.views import View
from django.views.generic import CreateView, FormView

from main_app.forms import DummyObjectForm, UserRegistrationForm
from main_app.helpers import app_login
from main_app.middlewares import get_current_db_name
from main_app.models import DummyObject, UserDatabaseTracker


class AppLoginRequiredMixin(LoginRequiredMixin):
    """
    Used to identify and ignore the failure cases. If the
    connection is not present.
    """

    def dispatch(self, request, *args, **kwargs):

        try:

            if request.user and request.user.is_authenticated:
                return super(AppLoginRequiredMixin, self).dispatch(
                    request, *args, **kwargs
                )

        except ConnectionDoesNotExist:
            pass

        return redirect(settings.LOGIN_URL)


class PingView(AppLoginRequiredMixin, CreateView):
    """Just a ping view. Used to create the dummy objects also for demo."""

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
    """App view for handling login logic."""

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
        """
        Database has to be created. We have skipped all form of model level
        validations for now and implemented it in terms of delete.
        """

        # let username be both | login happens through username
        username = form.cleaned_data["username"]

        # create and handle the database
        UserDatabaseTracker.objects.filter(user_identifier=username).delete()
        tracker = UserDatabaseTracker.objects.create(
            user_identifier=username, database_name=username
        )
        tracker.setup_database_and_configurations()

        # create the user on the user's database
        get_user_model().objects.using(tracker.db).filter(username=username).delete()
        get_user_model().objects.create_user(**form.cleaned_data, use_db=tracker.db)

        return super(UserRegistrationView, self).form_valid(form=form)


class AppLogoutView(AppLoginRequiredMixin, View):
    """View to log out the user."""

    def get(self, request, *args, **kwargs):
        """Handle on get."""

        logout(request)
        return redirect(settings.LOGIN_URL)
