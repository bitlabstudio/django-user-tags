"""
This ``urls.py`` is only used when running the tests via ``runtests.py``.
As you know, every app must be hooked into yout main ``urls.py`` so that
you can actually reach the app's views (provided it has any views, of course).

"""
from django.conf.urls.defaults import include, patterns, url


urlpatterns = patterns('',
    url(r'^', include('user_tags.tests.test_app.urls')),
    url(r'^jasmine/', include('django_jasmine.urls')),
)
