from user.models import User
from event.models import Event
from booking.models import Booking
from utilities.custom import custom_response
from rest_framework import status
from datetime import date
from booking.serializers import BookingSerializer
from django.db.models import F

def user_event_register(request):

    if request.method != 'POST':
        return custom_response(
            "Method not allowed. Allowed: POST",
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
        
    user_id = request.data.get('user_id')
    event_id = request.data.get('event_id')
    user_obj = User.objects.filter(pk=user_id).first()
    if not user_obj:
        return custom_response("User not found", 404)

    event_obj = Event.objects.filter(pk=event_id).first()
    if not event_obj:
        return custom_response("Event not found", 404)

    if Booking.objects.filter(user=user_obj, event=event_obj).exists():
        return custom_response("User already registered", 400)

    if event_obj.date < date.today():
        return custom_response("This event has already expired !", 400)

    if event_obj.available_seats <= 0:
        return custom_response("No seats available", 400)

    new_booking = Booking.objects.create(
        user=user_obj, 
        event=event_obj, 
        is_active=True
    )
    
    event_obj.available_seats = F('available_seats') - 1
    event_obj.save()
    serializer = BookingSerializer(new_booking)
    
    return custom_response("Registration successful", 201, serializer.data)