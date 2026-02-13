from event.models import Event
from .serializers import EventSerializer
from utilities.custom import custom_response
from rest_framework import status

def get_all_events():
    events_id = Event.objects.all()
    serializer = EventSerializer(events_id, many=True)
    return custom_response("Events retrieved successfully", status.HTTP_200_OK, serializer.data)