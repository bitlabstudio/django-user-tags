"""Utilities for creating test objects related to the ``user_tags`` app."""
from django.contrib.contenttypes.models import ContentType

import factory

from django_libs.tests.factories import UserFactory

from user_tags.models import TaggedItem, UserTag, UserTagGroup
from user_tags.tests.test_app.models import DummyModel


class DummyModelFactory(factory.Factory):
    """Creates ``DummyModel`` objects."""
    FACTORY_FOR = DummyModel
    name = 'dummy'


class TaggedItemFactory(factory.Factory):
    """Creates ``TaggedItem`` objects."""
    FACTORY_FOR = TaggedItem

    @classmethod
    def _prepare(cls, create, **kwargs):
        if create:
            dummy_model = DummyModelFactory.create()
            user_tag = UserTagFactory.create()
        else:
            dummy_model = DummyModelFactory.build()
            user_tag = UserTagFactory.build()

        item = super(TaggedItemFactory, cls)._prepare(False, **kwargs)
        if create:
            item.object_id = dummy_model.pk
            item.content_type = ContentType.objects.get_for_model(dummy_model)
            item.save()
            item.user_tags.add(user_tag)
        return item


class UserTagFactory(factory.Factory):
    """Creates ``UserTag`` objects."""
    FACTORY_FOR = UserTag

    user_tag_group = factory.LazyAttribute(lambda u: UserTagGroupFactory())
    text = 'sunny'


class UserTagGroupFactory(factory.Factory):
    """Creates ``UserTagGroup`` objects."""
    FACTORY_FOR = UserTagGroup

    user = factory.LazyAttribute(lambda u: UserFactory())
    name = 'weather'
