# Django - Shared App & Isolated Databases

An app that demonstrates the implementation of: `One Database Per User/Customer`.
The logic is handled in a single application instance.

In other words, each user should have their own database. Most SaaS products run in this architecture of data handling.

![Imgur](https://i.imgur.com/308fQMK.png)

### Working Of The Logic:

1. There is a centralized `routing-table` which points `user1` to `database1`.
2. While user creation, the routing-table instance is created on the default database.
3. The database is created dynamically on runtime for the user. The user instance is then created on the user specific database.
4. While login, the routing table is searched with the `username` or the unique identifier.
5. Depending on the database where the user's data is stored. The auth credentials are checked and then authenticated.
6. After authentication, the database to be used is set on the `local-thread`.
7. We have customised the `database-router` to get the data from the `local-thread` and query accordingly.
8. We have also used `cookies` to persist the user's auth and related data.


### Prerequisites

1. Python3.9.6
2. Virtualenv


### Getting Started Locally

1. Create a virtual environment in the project root using `virtualenv -p python3 venv`.
2. Activate the environment & install the packages inside `requirements.txt` file.
3. Use [pre-commit](https://pre-commit.com/) to maintain code integrity. Run: `pre-commit install`.
4. Run the app using `python manage.py migrate && python manage.py runserver`.


### References Used

1. https://books.agiliq.com/projects/django-multi-tenant/en/latest/isolated-database.html
2. https://oroinc.com/b2b-ecommerce/blog/single-tenant-vs-multi-tenant/


Your thoughts, suggestions, feedback, comments and PR's are welcome 😊
