import os

SECRET_KEY = 'just-for-tests'
MIDDLEWARE_CLASSES = []

INSTALLED_APPS = (
    "django.contrib.contenttypes",
    "django_unsigned_fields",
    "tests",
    "tests_with_migrations",
)

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
