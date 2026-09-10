from django.contrib import admin
from .models import Trigger, NotificationTemplate


@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'slug',
        'is_active',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'name',
        'slug',
    )


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):

    list_display = (
        'trigger',
        'channel',
        'subject',
        'is_active',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'trigger',
        'channel',
        'is_active',
    )

    search_fields = (
        'subject',
        'content',
    )