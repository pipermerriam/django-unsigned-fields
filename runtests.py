import os
import sys

from django.conf import settings

if os.environ.get('TRAVIS'):
    if os.environ.get('DATABASE_ENGINE') == 'django.db.backends.postgresql_psycopg2':
        os.environ.setdefault('DATABASE_USER', 'postgres')
    if os.environ.get('DATABASE_ENGINE') == 'django.db.backends.mysql':
        os.environ.setdefault('DATABASE_USER', 'root')
    os.environ.setdefault('DATABASE_USER', 'test_db')

DATABASES = {
    "default": {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_NAME', 'test_db'),
        'USER': os.environ.get('DATABASE_USER', 'root'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', ''),
    }
}


settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES=DATABASES,
    ROOT_URLCONF="django_unsigned_fields.urls",
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django_unsigned_fields",
        "tests",
        "tests_with_migrations",
    ],
    SITE_ID=1,
    NOSE_ARGS=['-s'],
    MIDDLEWARE_CLASSES=[],
)

try:
    import django
    setup = django.setup
except AttributeError:
    pass
else:
    setup()

from django_nose import NoseTestSuiteRunner


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
