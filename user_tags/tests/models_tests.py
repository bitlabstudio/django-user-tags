"""Tests for the models of the ``user_tags`` app."""
from django.test import TestCase

from user_tags.tests import factories


class TaggedItemTestCase(TestCase):
    def test_instantiation_and_save(self):
        item = factories.TaggedItemFactory()
        self.assertTrue(str(item))


class UserTagTestCase(TestCase):
    def test_instantiation_and_save(self):
        item = factories.UserTagFactory()
        self.assertTrue(str(item))


class UserTagGroupTestCase(TestCase):
    def test_instantiation_and_save(self):
        item = factories.UserTagGroupFactory()
        self.assertTrue(str(item))
