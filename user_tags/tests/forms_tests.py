"""Tests for the forms of the ``user_tags`` app."""
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from django_libs.tests.factories import UserFactory

from user_tags.tests.test_app.forms import DummyModelForm
from user_tags.models import TaggedItem, UserTag, UserTagGroup


class UserTagsFormMixinTestCase(TestCase):
    """Tests for the ``UserTagsFormMixin`` mixin class."""
    longMessage = True

    def setUp(self):
        """Creates a user and valid set of form data."""
        self.user = UserFactory()
        self.data = {
            'name': 'dummy',
            'tags': 'great day,family, cinema ',
            'global_tags': 'foo, bar',
        }

    def test_adds_fields_to_the_form(self):
        """
        A form that inherits from ``UserTagsFormMixin`` should have the
        fields that are defined on the model's ``TAG_FIELDS`` options dict
        as form fields.

        """
        form = DummyModelForm(self.user)
        self.assertTrue('tags' in form.fields)
        self.assertEqual(form.fields['tags'].help_text.encode(), b'Help text')
        self.assertTrue('global_tags' in form.fields)

    def test_form_valid(self):
        """Form should be valid when valid data is given."""
        form = DummyModelForm(self.user, data=self.data)
        self.assertTrue(form.is_valid())

    def test_save_returns_instance(self):
        """
        Save should return the saved instance when creating a new object.

        """
        form = DummyModelForm(self.user, data=self.data)
        instance = form.save()
        self.assertTrue(instance.pk)

    def test_creates_tag_group(self):
        """
        If the user has entered tags for a given tag field, the correct
        user tags related objects should be created.

        """
        form = DummyModelForm(self.user, data=self.data)
        instance = form.save()

        tag_group = UserTagGroup.objects.get(name='tags')
        user_tags = UserTag.objects.filter(user_tag_group=tag_group)
        self.assertEqual(user_tags.count(), 3)

        global_tag_group = UserTagGroup.objects.get(name='global_tags')
        global_tags = UserTag.objects.filter(user_tag_group=global_tag_group)
        self.assertEqual(global_tags.count(), 2)

        tagged_item = TaggedItem.objects.get(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk)
        self.assertEqual(tagged_item.user_tags.all().count(), 5)

    def test_tag_group_without_user(self):
        """
        For a tag group that has ``'with_user':  False`` in the ``TAG_FIELDS``
        option dict, the created tag group should not be bound to any user.

        """
        form = DummyModelForm(self.user, data=self.data)
        form.save()
        global_tag_group = UserTagGroup.objects.get(name='global_tags')
        self.assertEqual(global_tag_group.user, None)

    def test_form_should_be_valid_when_instance_given(self):
        """
        When instantiated with an instance, the form should, of course,
        be valid.

        """
        form = DummyModelForm(self.user, data=self.data)
        instance = form.save()
        form = DummyModelForm(self.user, data=self.data, instance=instance)
        self.assertTrue(form.is_valid())

    def test_save_instance_re_creates_everything(self):
        """
        When instantiated with an instance that already has tags, those tags
        should be deleted when the form is saved. Only the newly submitted
        tags will get re-created.

        In this test we don't touch the two existing 'global_tags' but we
        re-submit two new 'tags' (before that group had three tags). So in
        total we should have four tags now, not five.

        """
        form = DummyModelForm(self.user, data=self.data)
        instance = form.save()
        data2 = self.data.copy()
        data2.update({'tags': 'family, cinema', })
        form = DummyModelForm(self.user, data=data2, instance=instance)
        instance = form.save()
        tagged_item = TaggedItem.objects.get(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk)
        self.assertEqual(tagged_item.user_tags.all().count(), 4)

    def test_get_user_from_instance(self):
        """
        If form was not instanciated with user parameter, it will try to get
        the user from the instance.

        """
        form = DummyModelForm(self.user, data=self.data)
        instance = form.save()
        instance.user = self.user
        form = DummyModelForm(instance=instance, data=self.data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_get_user_method(self):
        """
        If form was not instantiated with suer parameter and the instance does
        not have a user field, it will try to call a ``get_user`` method on
        the form.

        """
        form = DummyModelForm(self.user, data=self.data)
        instance = form.save()
        form = DummyModelForm(instance=instance, data=self.data)

        def get_user():
            return self.user

        form.get_user = get_user
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_no_user_given(self):
        """
        If form was not instanciated with user parameter and instance has no
        user attribute and not get_user method, so be it. This tag is probably
        supposed to be global to the project.

        """
        form = DummyModelForm(self.user, data=self.data)
        instance = form.save()

        form = DummyModelForm(instance=instance, data=self.data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_no_tags(self):
        form = DummyModelForm(self.user, data=self.data)
        instance = form.save()

        TaggedItem.objects.all().delete()
        form = DummyModelForm(instance=instance, data=self.data)
        self.assertTrue(form.is_valid())

    def test_split_tags(self):
        tags = DummyModelForm.split_tags('great day,family, cinema, ')
        self.assertEqual(len(tags), 3)
        self.assertEqual(tags[0], 'great day')
        self.assertEqual(tags[1], 'family')
        self.assertEqual(tags[2], 'cinema')

    def test_adds_tag_list_to_form(self):
        """
        Should add the available tags for each given tag field to the form.

        This enables users to do this in their templates::

            $(document).ready(function() {
                $('#id_skills').tagit({
                    allowSpaces: true
                    ,availableTags:
                      {{ form.available_tags_technical_skills|safe }}
                    ,caseSensitive: false
                    ,removeConfirmation: true
                });
            }

        """
        form = DummyModelForm(self.user, data=self.data)
        form.save()
        result = form.tags_tags_values()
        self.assertEqual(result, '["cinema", "family", "great day"]')
        result = form.global_tags_tags_values()
        self.assertEqual(result, '["bar", "foo"]')

        user2 = UserFactory()
        form = DummyModelForm(user2)
        result = form.tags_tags_values()
        self.assertEqual(result, '[]', msg=(
            'A user should not be able to see the private tags of another'
            ' user.'))

        form = DummyModelForm()
        result = form.tags_tags_values()
        self.assertEqual(result, '[]', msg=(
            'An anonymous user should not be able to see user specific tags.'))
