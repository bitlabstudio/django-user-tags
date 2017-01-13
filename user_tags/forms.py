"""Forms for the ``user_tags`` app."""
import json

from django import forms
from django.contrib.contenttypes.models import ContentType

from user_tags.models import UserTagGroup, UserTag, TaggedItem


def add_tags_values(cls, field_name, settings):
    """
    Dynamically adds a ``get_tags_values`` method to the form's fields.

    :cls: The form instance that should get the new method. Should be a form
      instance with a model that has a ``TAG_FIELDS`` attribute.
    :field_name: The name of the original field.
    :settings: The dictionary with additional settings needed for adding the
      new method.

    """
    def inner_function(self):
        """
        The actual code of the function that returns the crowdsourced values.

        """
        this = inner_function
        this_name = this.__name__
        original_name = this_name.replace('_tags_values', '')
        model = self.__class__.Meta.model
        field_settings = model.TAG_FIELDS[original_name]

        qs_kwargs = {'name': original_name, }
        if field_settings['with_user']:
            user = self._get_user(self.instance)
            qs_kwargs.update({'user': user, })
        try:
            tag_group = UserTagGroup.objects.get(**qs_kwargs)
        except UserTagGroup.DoesNotExist:
            tag_group = None
            tag_list = []
        if tag_group:
            tags = tag_group.usertag_set.all()
            tag_list = [tag.text for tag in tags]
        return json.dumps(tag_list)

    inner_function.__doc__ = (
        'Returns the tags values for the {0} field'.format(
            field_name))
    inner_function.__name__ = '{0}_tags_values'.format(field_name)
    setattr(cls.__class__, inner_function.__name__, inner_function)


class UserTagsFormMixin(object):
    """
    Adds all fields declared in the model's TAG_FIELDS attribute to the form.

    IMPORTANT: If your tag field has ``with_user=True`` you must make sure to
    add ``self.user = user`` in your form's ``__init__`` method. Your form
    would most probably need to be instantiated with a mandatory parameter
    ``user``.

    """
    def __init__(self, *args, **kwargs):
        """
        If the model has a ``TAG_FIELDS`` attribute, this constructor adds
        a form field to the form for each tag field.

        """
        super(UserTagsFormMixin, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        for field_name, option_dict in self.Meta.model.TAG_FIELDS.items():
            verbose_name = option_dict.get('verbose_name', field_name)
            help_text = option_dict.get('help_text', None)
            self.fields[field_name] = forms.CharField(
                required=False,
                max_length=4000,
                label=verbose_name,
                help_text=help_text,
                widget=forms.TextInput(attrs={'class': 'tagItInput'}),
            )

            add_tags_values(self, field_name, option_dict)
            if not instance:
                continue

            try:
                tagged_item = TaggedItem.objects.get(
                    content_type=ContentType.objects.get_for_model(instance),
                    object_id=instance.pk)
            except TaggedItem.DoesNotExist:
                continue

            user_tags = tagged_item.user_tags.filter(
                user_tag_group__name=field_name)
            self.initial[field_name] = ', '.join(
                [tag.text for tag in user_tags])

    def _get_user(self, instance):
        """Tries to retrieve the user from the form."""
        if hasattr(self, 'user'):
            user = self.user
        elif hasattr(instance, 'user'):
            user = instance.user
        elif hasattr(self, 'get_user'):
            user = self.get_user()
        else:
            user = None
        return user

    def save(self, *args, **kwargs):
        """Saves all tags for this instance."""
        instance = super(UserTagsFormMixin, self).save(*args, **kwargs)
        tagged_item_user = self._get_user(instance)
        tagged_items = TaggedItem.objects.filter(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id)
        tagged_items.delete()
        tagged_item = TaggedItem(content_object=instance)
        tagged_item.save()
        for field_name, options_dict in self.Meta.model.TAG_FIELDS.items():
            with_user = options_dict.get('with_user', True)
            self.save_tags(tagged_item_user, tagged_item, field_name,
                           with_user, self.cleaned_data[field_name])
        return instance

    def save_tags(self, user, tagged_item, tag_field, with_user, tag_data):
        try:
            group = UserTagGroup.objects.get(name=tag_field)
        except UserTagGroup.DoesNotExist:
            the_user = None
            if with_user:
                the_user = user
            group = UserTagGroup(user=the_user, name=tag_field)
            group.save()
        tags = self.split_tags(tag_data)
        for tag in tags:
            try:
                user_tag = UserTag.objects.get(user_tag_group=group, text=tag)
            except UserTag.DoesNotExist:
                user_tag = UserTag(user_tag_group=group, text=tag)
                user_tag.save()
            tagged_item.user_tags.add(user_tag)

    @staticmethod
    def split_tags(tag_data):
        tags = []
        for tag in tag_data.split(','):
            tag = tag.strip()
            if tag and tag not in tags:
                tags.append(tag)
        return tags
