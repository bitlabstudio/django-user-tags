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
    pip install South

If you want to install the latest stable release from PyPi::

    $ pip install django-user-tags

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-user-tags.git#egg=user_tags

Add ``user_tags`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'user_tags',
    )

Don't forget to migrate your database::

    ./manage.py migrate user_tags

Add jQuery and jQuery UI and tag-it to your base template or at least to the
template that should display forms with tag fields::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/jquery-ui.min.js" type="text/javascript" charset="utf-8"></script>
    <script src="{{ STATIC_URL }}user_tags/js/tag-it.js" type="text/javascript" charset="utf-8"></script>

Also add a jQuery UI theme and the tag-it theme to your template::

    <link rel="stylesheet" type="text/css" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1/themes/flick/jquery-ui.css">
    <link href="{{ STATIC_URL }}user_tags/css/jquery.tagit.css" rel="stylesheet" type="text/css">

Usage
-----

First you need to modify the model that should be able to hold tags::

    class YourModel(models.Model):
        TAG_FIELDS = {
            'tags': {
                'verbose_name': _('Tags'),
                'help_text': _('Help text'),
                'with_user': True,
            },
            'global_tags': {
                'verbose_name': _('Global Tags'),
                'with_user': False,
            }
        }

``TAG_FIELDS`` is a dictionary of dictionaries. The dictionaries can have the
following keys:

1. **key in main dict**. This will be the name of the tag group in the
   database and also the form field's name.
2. **verbose_name**. This will be the label of the form field. If not provided
   it will be the same as ``name``.
3. **help_text**. This will be the help text of the form field.
4. **with user**. If ``True``, the item that gets tagged must have a ForeignKey
   to a ``User`` object or provide a ``get_user`` method. If ``False`` we
   assume that the tags for this item are global.

Next you would create a ``ModelForm`` for your taggable model::

    from django import forms
    from user_tags.forms import UserTagsFormMixin
    from your_app.models import YourModel

    class YourModelForm(UserTagsFormMixin, forms.ModelForm):
        class Meta:
            model = DummyModel

The ``UserTagsFormMixin`` will do the magic for you and add a form field for
every item in ``TAG_FIELDS`` on your model. These fields will have a class
``tagItInput``. Additionally the mixin will add a method
``fieldname_tags_values`` to the form (for each of your tag fields) which will
return the available tags for that field::

    <script type="text/javascript">
    $(document).ready(function() {
        $("#id_fieldname").tagit({
            allowSpaces: true
            ,availableTags: {{ form.fieldname_tags_values|safe }}
            ,caseSensitive: false
        });
    });
    </script>

This is just a sane set of settings that we like to use. You can of course
tweak that to your liking. See the `tag-it documentation <https://github.com/aehlke/tag-it>`_
for further reference.

Settings
--------

USER_TAG_RELATED_NAME
+++++++++++++++++++++

If for some reason one of your models already has a foreign key to
``ContentType`` with a related name of ``user_tags_tagged_items`` you can
change the related name used  by ``django-user-tags`` using this setting.

Default: 'user_tags_tagged_items'

Contribute
----------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-user-tags
    $ pip install -r requirements.txt
    $ ./user_tags/tests/runtests.sh
    # You should get no failing tests

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ ./user_tags/tests/runtests.sh
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
