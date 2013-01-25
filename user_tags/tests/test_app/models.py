"""Dummy model needed for tests."""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DummyModel(models.Model):
    """Dummy model needed for testing purposes."""
    TAG_FIELDS = {
        'tags': {
            'verbose_name': _('Tags'),
            'help_text': _('Help text'),
            'with_user': True,
        },
        'global_tags': {
            'verbose_name': _('Global Tags'),
            'with_user': False,
        }
    }

    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'),
    )
