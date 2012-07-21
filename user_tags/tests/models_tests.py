"""Tests for the models of the ``user_tags`` app."""
from django.test import TestCase

from user_tags.tests.factories import TaggedItemFactory


class UserTagsTestCase(TestCase):
    """Tests for the model classes of the ``user_tags`` apps."""
    def test_instantiation_and_save(self):
        item = TaggedItemFactory.create()
        self.assertTrue(item.pk)
