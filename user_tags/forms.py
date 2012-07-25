"""Forms for the ``user_tags`` app."""
from django import forms
from django.contrib.contenttypes.models import ContentType

from user_tags.models import UserTagGroup, UserTag, TaggedItem


class UserTagsFormMixin(object):
    """
    Adds all fields declared in the model's TAG_FIELDS attribute to the form.

    """
    def __init__(self, *args, **kwargs):
        """
        If the model has a ``TAG_FIELDS`` attribute, this constructor adds
        a form field to the form for each tag field.

        """
        super(UserTagsFormMixin, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        for option_dict in self.Meta.model.TAG_FIELDS:
            field_name = option_dict['name']
            verbose_name = option_dict.get('verbose_name', field_name)
            help_text = option_dict.get('help_text', None)
            self.fields[field_name] = forms.CharField(
                required=False,
                max_length=4000,
                label=verbose_name,
                help_text=help_text,
                widget=forms.TextInput(attrs={'class': 'tagItInput'}),
            )

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

    def save(self, *args, **kwargs):
        """Saves all tags for this instance."""
        instance = super(UserTagsFormMixin, self).save(*args, **kwargs)

        if hasattr(self, 'user'):
            tagged_item_user = self.user
        elif hasattr(instance, 'user'):
            tagged_item_user = instance.user
        elif hasattr(self, 'get_user'):
            tagged_item_user = self.get_user()
        else:
            tagged_item_user = None

        tagged_items = TaggedItem.objects.filter(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id)
        tagged_items.delete()
        tagged_item = TaggedItem(content_object=instance)
        tagged_item.save()
        for options_dict in self.Meta.model.TAG_FIELDS:
            field_name = options_dict['name']
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
            if tag and not tag in tags:
                tags.append(tag)
        return tags
