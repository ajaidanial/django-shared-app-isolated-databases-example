from django.urls import path

from . import views

urlpatterns = [
    path("ping/", views.ping_view, name="ping_view"),
    path("register/", views.UserRegistrationView.as_view(), name="register_view"),
    path("login/", views.UserLoginView.as_view(), name="login_view"),
]
