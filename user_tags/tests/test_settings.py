"""Settings that need to be set in order to run the tests."""
import os

DEBUG = True

DATABASES={
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF='user_tags.tests.urls'

STATIC_URL='/static/'

STATIC_ROOT=os.path.join(__file__, '../../static/')

STATICFILES_DIRS=(
    os.path.join(__file__, 'test_static'),
)

TEMPLATE_DIRS=(
    os.path.join(os.path.dirname(__file__), '../templates'),
)

JASMINE_TEST_DIRECTORY=os.path.join(__file__, 'jasmine_tests')

COVERAGE_REPORT_HTML_OUTPUT_DIR=os.path.join(
    os.path.dirname(__file__), 'coverage')

COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'test_app$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
]

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django_jasmine',
]

INTERNAL_APPS = [
    'django_nose',
    'user_tags.tests.test_app',
    'user_tags',
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS
