"""Utilities for creating test objects related to the ``user_tags`` app."""
import factory

from django_libs.tests.factories import UserFactory

from user_tags.models import TaggedItem, UserTag, UserTagGroup
from user_tags.tests.test_app.models import DummyModel


class DummyModelFactory(factory.Factory):
    """Creates ``DummyModel`` objects."""
    class Meta:
        model = DummyModel

    name = 'dummy'


class TaggedItemFactory(factory.Factory):
    """Creates ``TaggedItem`` objects."""
    class Meta:
        model = TaggedItem

    content_object = factory.SubFactory(DummyModelFactory)


class UserTagFactory(factory.Factory):
    """Creates ``UserTag`` objects."""
    class Meta:
        model = UserTag

    user_tag_group = factory.LazyAttribute(lambda u: UserTagGroupFactory())
    text = 'sunny'


class UserTagGroupFactory(factory.Factory):
    """Creates ``UserTagGroup`` objects."""
    class Meta:
        model = UserTagGroup

    user = factory.LazyAttribute(lambda u: UserFactory())
    name = 'weather'
