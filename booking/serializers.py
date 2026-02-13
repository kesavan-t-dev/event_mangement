from rest_framework import serializers
from .models import Booking
from event.serializers import EventSerializer

class BookingSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True) 
    class Meta:
        model = Booking
        fields = ['booking_id','user','event']