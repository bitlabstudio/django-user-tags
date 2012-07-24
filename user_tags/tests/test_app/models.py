"""Dummy model needed for tests."""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DummyModel(models.Model):
    """Dummy model needed for testing purposes."""
    TAG_FIELDS = [
        ('tags', _('Tags'), True),
        ('global_tags', _('Global Tags'), False),
    ]

    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'),
    )
