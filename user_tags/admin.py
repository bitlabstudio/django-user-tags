"""Admin classes for the ``user_tags`` app."""
from django.contrib import admin

from user_tags.models import TaggedItem, UserTag, UserTagGroup


class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', ]


class UserTagAdmin(admin.ModelAdmin):
    list_display = ['user_tag_group', 'text', ]


class UserTagGroupAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', ]


admin.site.register(TaggedItem, TaggedItemAdmin)
admin.site.register(UserTag, UserTagAdmin)
admin.site.register(UserTagGroup, UserTagGroupAdmin)
