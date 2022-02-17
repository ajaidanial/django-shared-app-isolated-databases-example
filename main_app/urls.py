from django.urls import path

from . import views

urlpatterns = [
    # authenticated views
    path("ping/", views.PingView.as_view(), name="ping_view"),
    path("logout/", views.AppLogoutView.as_view(), name="logout_view"),
    # non authenticated views
    path("register/", views.UserRegistrationView.as_view(), name="register_view"),
    path("login/", views.UserLoginView.as_view(), name="login_view"),
]
