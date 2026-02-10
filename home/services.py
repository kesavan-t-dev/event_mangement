from .models import Organiser, Event, User, Booking
from .serializers import OrganiserSerializer, EventSerializer, UserSerializer, BookingSerializer

def get_all_organisers():
    return OrganiserSerializer(Organiser.objects.all(), many=True).data

def create_organiser(data):
    serializer = OrganiserSerializer(data=data)
    if serializer.is_valid():
        instance = serializer.save()
        return serializer.data, None
    return None, serializer.errors


def get_all_events():
    return EventSerializer(Event.objects.all(), many=True).data

def create_event(data):
    serializer = EventSerializer(data=data)
    if serializer.is_valid():
        instance = serializer.save()
        return serializer.data, None
    return None, serializer.errors


def get_all_users():
    return UserSerializer(User.objects.all(), many=True).data

def create_user(data):
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        instance = serializer.save()
        return serializer.data, None
    return None, serializer.errors


def get_all_bookings():
    return BookingSerializer(Booking.objects.all(), many=True).data

def register_user_for_event(data):
    serializer = BookingSerializer(data=data)
    if serializer.is_valid():
        instance = serializer.save()
        return serializer.data, None
    return None, serializer.errors
