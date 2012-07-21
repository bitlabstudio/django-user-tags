"""Tests for the forms of the ``user_tags`` app."""
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from django_libs.tests.factories import UserFactory

from user_tags.forms import DummyModelForm
from user_tags.models import TaggedItem, UserTag, UserTagGroup


class UserTagsFormMixinTestCase(TestCase):
    """Tests for the ``UserTagsFormMixin`` mixin class."""
    def test_adds_fields_to_the_form(self):
        user = UserFactory.build()
        form = DummyModelForm(user)
        self.assertTrue('tags' in form.fields)
        self.assertTrue('mood' in form.fields)

    def test_save(self):
        user = UserFactory.create()
        data = {
            'name': 'dummy',
            'tags': 'great day,family, cinema ',
            'mood': 'energetic',
        }
        form = DummyModelForm(user, data=data)
        self.assertTrue(form.is_valid(), msg=(
            'Form should be valid when valid data is given'))

        instance = form.save()
        self.assertTrue(instance.pk, msg=(
            'Save should return the saved instance when creating a new'
            ' object'))

        tag_group = UserTagGroup.objects.get(name='tags')
        self.assertTrue(tag_group, msg=(
            'Save should create a UserTagGroup named `tags`'))

        user_tags = UserTag.objects.filter(user_tag_group=tag_group)
        self.assertEqual(user_tags.count(), 3, msg=(
            'Save should create UserTag objects `great day`, `family` and'
            ' `cinema`'))

        tagged_item = TaggedItem.objects.get(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk)
        self.assertEqual(tagged_item.user_tags.all().count(), 4, msg=(
            'Save should create a TaggedItem and add all UserTags to'
            ' that item'))

        data2 = data.copy()
        data2.update({'tags': 'family, cinema', })
        form = DummyModelForm(user, data=data2, instance=instance)
        self.assertTrue(form.is_valid(), msg=(
            'Form should be valid when valid data and instance is given'))

        instance = form.save()
        tagged_item = TaggedItem.objects.get(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk)
        self.assertEqual(tagged_item.user_tags.all().count(), 3, msg=(
            'When saving existing tags for that instance should be deleted'
            ' and re-created'))

        instance.user = user
        form = DummyModelForm(instance=instance, data=data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save(), msg=(
            'If form was not instanciated with user parameter, it will try'
            ' to get the user from the instance'))

        delattr(instance, 'user')
        form = DummyModelForm(instance=instance, data=data)

        def get_user():
            return user

        form.get_user = get_user
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save(), msg=(
            'If form was not instanciated with user parameter and instance'
            ' has no user attribute, it will try to call get_user on the'
            ' form'))

        form = DummyModelForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertRaises(Exception, form.save)

    def test_split_tags(self):
        tags = DummyModelForm.split_tags('great day,family, cinema, ')
        self.assertEqual(len(tags), 3)
        self.assertEqual(tags[0], 'great day')
        self.assertEqual(tags[1], 'family')
        self.assertEqual(tags[2], 'cinema')
