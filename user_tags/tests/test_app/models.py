"""Dummy model needed for tests."""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DummyModel(models.Model):
    """Dummy model needed for testing purposes."""
    TAG_FIELDS = [
        ('tags', _('Tags')),
        ('mood', _('Mood')),
    ]

    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'),
    )
