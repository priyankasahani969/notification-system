from django.db import models
from django.contrib.auth.models import User


class Trigger(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        max_length=100,
        unique=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class NotificationTemplate(models.Model):

    CHANNEL_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('web_push', 'Web Push'),
    ]

    trigger = models.ForeignKey(
        Trigger,
        on_delete=models.CASCADE,
        related_name='templates'
    )

    channel = models.CharField(
        max_length=20,
        choices=CHANNEL_CHOICES
    )

    subject = models.CharField(
        max_length=255,
        blank=True
    )

    content = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ('trigger', 'channel')

    def __str__(self):
        return f"{self.trigger.name} - {self.channel}"


class PushSubscription(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    endpoint = models.TextField(unique=True)

    p256dh = models.TextField()

    auth = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.endpoint[:50]    