from .models import Organiser, Event, User, Booking
from .serializers import OrganiserSerializer, EventSerializer, UserSerializer, BookingSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F

def get_all_organisers():
    organiser_id = Organiser.objects.all()
    serializer = OrganiserSerializer(organiser_id, many=True)
    return custom_response("Organisers retrieved successfully", status.HTTP_200_OK, serializer.data)

def get_all_events():
    events_id = Event.objects.all()
    serializer = EventSerializer(events_id, many=True)
    return custom_response("Events retrieved successfully", status.HTTP_200_OK, serializer.data)

def get_all_users():
    users_id = User.objects.all()
    serializer = UserSerializer(users_id, many=True)
    return custom_response("Users retrieved successfully", status.HTTP_200_OK, serializer.data)


def event_create(request):
    try:
        if request.method != 'POST':
            return custom_response(
                f"Method {request.method} not allowed. Allowed: POST",
                status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
        title = request.data.get('event_title')
        event_date = request.data.get('date')
        start_time = request.data.get('start_time')
        if Event.objects.filter(event_title=title, date=event_date, start_time=start_time).exists():
            return custom_response(
                f"An event is already scheduled", 
                400
            )

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response("Event created successfully", 201, serializer.data)
        
        return custom_response("Validation failed", 400, serializer.errors)

    except Exception as e:
        return custom_response(f"Internal server error: {str(e)}", 500)
    
def user_create(request):
    try:
        if request.method != 'POST':
            return custom_response(
                f"Method {request.method} not allowed. Allowed: POST",
                status.HTTP_405_METHOD_NOT_ALLOWED
            )

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response("User(s) created successfully", status.HTTP_201_CREATED, serializer.data)

        return custom_response("Validation failed", status.HTTP_400_BAD_REQUEST, serializer.errors)

    except Exception as e:
        return custom_response(f"Internal server error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR, serializer.errors)


def user_event_register(request):
    try:
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

        if event_obj.available_seat <= 0:
            return custom_response("No seats available", 400)

        new_booking = Booking.objects.create(
            user=user_obj, 
            event=event_obj, 
            is_active=True
        )
        
        event_obj.available_seat = F('available_seat') - 1
        event_obj.save()
        serializer = BookingSerializer(new_booking)
        
        return custom_response("Registration successful", 201, serializer.data)

    except Exception as e:
        return custom_response(f"Internal server error: {str(e)}", 500)

def event_update(request, id):
    try:
        if request.method != 'PUT':
            return custom_response(f"Method {request.method} not allowed. Allowed: PUT", 405)

        event_instance = Event.objects.filter(pk=id).first()
        if not event_instance:
            return custom_response("Event not found", 404)

        serializer = EventSerializer(event_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response("Event updated successfully", 200, serializer.data)
        
        return custom_response("Validation failed", 400, serializer.errors)

    except Exception as e:
        return custom_response(f"Internal server error: {str(e)}", 500)

def user_update(request, id):
    try:
        if request.method != 'PATCH':
            return custom_response(f"Method {request.method} not allowed. Allowed: PATCH", 405)

        user_instance = User.objects.filter(pk=id).first()
        if not user_instance:
            return custom_response("User not found", 404)

        serializer = UserSerializer(user_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response("User updated successfully", 200, serializer.data)
        
        return custom_response("Validation failed", 400, serializer.errors)

    except Exception as e:
        return custom_response(f"Internal server error: {str(e)}", 500)

def custom_response(message, status_code, data=None):
    return Response({
        "message": message,
        "status": status_code,
        "data": data if data is not None else {}
    }, status=status_code)

