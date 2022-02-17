from django.urls import path

from . import views

urlpatterns = [
    path("ping/", views.ping_view),
    path("register/", views.UserRegistrationView.as_view()),
]
