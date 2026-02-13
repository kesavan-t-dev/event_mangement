from .models import Organiser
from .serializers import OrganiserSerializer
from utilities.custom import custom_response
from rest_framework import status
from event.models import Event
from event.serializers import EventSerializer
from datetime import date
from datetime import datetime

def get_all_organisers():
    organiser_id = Organiser.objects.all()
    serializer = OrganiserSerializer(organiser_id, many=True)
    return custom_response("Organisers retrieved successfully", status.HTTP_200_OK, serializer.data)

def event_create(request):
    if request.method != 'POST':
        return custom_response(
            f"Method {request.method} not allowed. Allowed: POST",
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    title = request.data.get('event_title')
    event_date = request.data.get('date')
    start_time = request.data.get('start_time')
    date_obj = datetime.strptime(event_date, "%Y-%m-%d").date()
    if Event.objects.filter(event_title=title, date=event_date, start_time=start_time).exists():
        return custom_response(
            f"An event is already Booked !", 
            400
        )
    if date_obj < date.today():
        return custom_response(
            "Past date is not allowed",
            400
        )

    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response("Event created successfully", 201, serializer.data)
    
    return custom_response("Validation failed", 400, serializer.errors)