"""Models for the ``user_tags`` app."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class TaggedItem(models.Model):
    """
    This actually maps tags to real items.

    For example there might be a "WeatherEntry" object in the database, which
    has a tag group called "description" and tags called "sunny" and "rainy".

    The ``TaggedItem`` is the missing piece to link the user tag "sunny" to the
    "WeatherEntry" object in the database.

    :content_object: Can be any Django model object that should be tagged.
    :user_tag: One or many ``UserTag`` instances.

    """
    content_type = models.ForeignKey(
        ContentType,
        related_name=getattr(
            settings, 'USER_TAGS_RELATED_NAME', 'user_tags_tagged_items'),
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user_tags = models.ManyToManyField(
        'user_tags.UserTag',
        verbose_name=_('User tag'),
    )

    def __str__(self):
        return str(self.content_object)


@python_2_unicode_compatible
class UserTag(models.Model):
    """
    Belongs to a ``UserTagGroup`` and resembles a tag in that group.

    Each user tag inside a tag group must be unique in that group. This allows
    a user to rename a tag (i.e. to correct a typo) and have all of these tags
    updated immediately.

    :user_tag_group: A ``UserTagGroup`` instance.
    :text: The text of this tag, i.e. "sunny"

    """
    class Meta:
        unique_together = ('user_tag_group', 'text')

    user_tag_group = models.ForeignKey(
        'user_tags.UserTagGroup',
        verbose_name=_('User tag group'),
    )

    text = models.CharField(
        max_length=256,
        verbose_name=_('Text'),
    )

    def __str__(self):
        return self.text


@python_2_unicode_compatible
class UserTagGroup(models.Model):
    """
    Belongs to a ``User`` and resembles a group of tags.

    For example "weather" might be a group of tags with lot's of ``UserTag``
    objects like "sunny", "rainy" etc..

    :user: A ``User`` instance. Usually this should be set as it allows your
      users to add tags to things that do not overlap with tags from other
      user's things. If you want to use this app as a generic tagging solution
      that should just save tags for everyone project wide, this field can be
      empty.
    :name: The name of this tag group.

    """
    class Meta:
        unique_together = ('user', 'name')

    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        null=True, blank=True,
    )

    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'),
    )

    def __str__(self):
        return '{0} of {1}'.format(
            self.name, self.user and self.user.email or 'None')
