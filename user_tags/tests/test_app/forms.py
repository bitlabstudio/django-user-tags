from django import forms

from user_tags.forms import UserTagsFormMixin
from user_tags.tests.test_app.models import DummyModel


class DummyModelForm(UserTagsFormMixin, forms.ModelForm):
    """We need this to test the ``UserTagsFormMixin``."""
    class Meta:
        model = DummyModel
        fields = '__all__'

    def __init__(self, user=None, *args, **kwargs):
        if user is not None:
            self.user = user
        super(DummyModelForm, self).__init__(*args, **kwargs)
