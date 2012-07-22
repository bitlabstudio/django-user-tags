Django User Tags
================

**WORK IN PROGRESS. DO NOT USE THIS!**

A Django application for allowing users to add tags to any object. Each user's
tags are nicely separated so that the auto-suggest functionality will never
suggest tags that have been entered by a different user (unless you want so).

Installation
------------

You need to install the following prerequisites in order to use this app::

    pip install Django

If you want to install the latest stable release from PyPi::

    $ pip install django-user-tags

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-user-tags.git#egg=user_tags

Add ``user_tags`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'user_tags',
    )

Add jQuery and jQuery UI and tag-it to your base template::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/jquery-ui.min.js" type="text/javascript" charset="utf-8"></script>
    <script src="{{ STATIC_URL }}user_tags/js/tag-it.js" type="text/javascript" charset="utf-8"></script>

Add a jQuery UI theme and the tag-it theme to yout base template::

    <link rel="stylesheet" type="text/css" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1/themes/flick/jquery-ui.css">
    <link href="{{ STATIC_URL }}user_tags/css/jquery.tagit.css" rel="stylesheet" type="text/css">

Usage
-----

TODO: Describe usage

Contribute
----------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-online-docs
    $ pip install -r requirements.txt
    $ ./online_docs/tests/runtests.sh
    # You should get no failing tests

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ ./online_docs/tests/runtests.sh
    # You should still get no failing tests
    # Describe your change in the CHANGELOG.txt
    $ git add . && git commit
    $ git push origin feature_branch
    # Send us a pull request for your feature branch

Whenever you run the tests a coverage output will be generated in
``tests/coverage/index.html``. When adding new features, please make sure that
you keep the coverage at 100%.

If you are making changes that need to be tested in a browser (i.e. to the
CSS or JS files), you might want to setup a Django project, follow the
installation insttructions above, then run ``python setup.py develop``. This
will just place an egg-link to your cloned fork in your project's virtualenv.

Roadmap
-------

Check the issue tracker on github for milestones and features to come.
