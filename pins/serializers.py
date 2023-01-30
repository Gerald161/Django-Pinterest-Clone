from rest_framework import serializers
from .models import Pin


class pin_serializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = (
            'name', 'image'
        )