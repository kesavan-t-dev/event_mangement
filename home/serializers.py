from rest_framework import serializers
from .models import Organiser, Event, User, Booking

class OrganiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organiser
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
