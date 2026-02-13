from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = [
            'event_id',
            'organisers_id',
            'event_title',
            'event_type',
            'date',
            'location',
            'available_seats',
            'total_seats',
            'start_time'
        ]
