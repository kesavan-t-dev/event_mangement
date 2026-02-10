from rest_framework import serializers
from .models import Organiser, Event, User, Booking

class OrganiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organiser
        fields = ['organiser_id','name','phone','email']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'even_id',
            'organisers',
            'event_title',
            'event_type',
            'date',
            'location',
            'available_seat',
            'total_seats',
            'start_time'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id','name','phone','email']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['booking_id','user','event']
