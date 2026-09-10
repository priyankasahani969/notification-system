from rest_framework import serializers
from .models import Trigger,NotificationTemplate


class TriggerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trigger
        fields = '__all__'

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'