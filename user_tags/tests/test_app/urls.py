"""
URLs for the test_app of `django-user-tags`.

Allows us to run `./manage.py runserver` and see a form that uses the tag
functionality. This helps testing the JavaScript related parts of this app
without needing to setup a full blown Django project.

"""
from django.conf.urls.defaults import patterns, url

from user_tags.tests.test_app.views import TestView


urlpatterns = patterns(
    '',
    url(r'^$', TestView.as_view(), name='user_tags_test_view'),
)
