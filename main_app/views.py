from django.http import HttpResponse


def ping_view(request):
    """Just a ping view."""

    return HttpResponse("Pong!")
