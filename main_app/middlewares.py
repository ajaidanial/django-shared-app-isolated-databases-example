import threading

THREAD_LOCAL = threading.local()


def get_current_db_name():
    """Gets which db for the user from the thread."""

    return getattr(THREAD_LOCAL, "use_db", None)


def set_db_for_router(db):
    """Sets which db for user to the thread."""

    setattr(THREAD_LOCAL, "use_db", db)


class AppIsolatedDatabasesHelperMiddleware:
    """Sets the necessary data to the response, getting and hanlding the same."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Get and set the cookies for using later."""

        set_db_for_router(request.COOKIES.get("use_db", None))

        response = self.get_response(request)

        response.set_cookie(key="use_db", value=get_current_db_name())

        return response
