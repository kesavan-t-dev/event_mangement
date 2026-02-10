from .models import Organiser, Event, User, Booking
from .serializers import OrganiserSerializer, EventSerializer, UserSerializer, BookingSerializer




def get_all_organisers():
    return OrganiserSerializer(Organiser.objects.all(), many=True).data

def get_all_events():
    return EventSerializer(Event.objects.all(), many=True).data

def get_all_users():
    return UserSerializer(User.objects.all(), many=True).data

def get_all_bookings():
    return BookingSerializer(Booking.objects.all(), many=True).data
