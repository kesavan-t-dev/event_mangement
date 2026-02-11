from .models import Organiser, Event, User, Booking
from .serializers import OrganiserSerializer, EventSerializer, UserSerializer, BookingSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F

def get_all_organisers():
    organisers = Organiser.objects.all()
    serializer = OrganiserSerializer(organisers, many=True)
    return custom_response("Organisers retrieved successfully", status.HTTP_200_OK, serializer.data)

def get_all_events():
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return custom_response("Events retrieved successfully", status.HTTP_200_OK, serializer.data)

def get_all_users():
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return custom_response("Users retrieved successfully", status.HTTP_200_OK, serializer.data)


def update_organiser(request, phone):
    try:
        if request.method != 'PATCH':
            return custom_response(
                f"Method {request.method} not allowed. Allowed: PATCH",
                status.HTTP_405_METHOD_NOT_ALLOWED
            )

        organiser = Organiser.objects.get(phone=phone)

        serializer = OrganiserSerializer(organiser, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                "Organiser updated successfully (PATCH)",
                status.HTTP_200_OK,
                serializer.data
            )

        return custom_response("Validation failed", status.HTTP_400_BAD_REQUEST, serializer.errors)

    except Organiser.DoesNotExist:
        return custom_response("Organiser not found", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return custom_response(f"Internal server error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)


def event_create(request):
    try:
        if request.method != 'POST':
            return custom_response(
                f"Method {request.method} not allowed. Allowed: POST",
                status.HTTP_405_METHOD_NOT_ALLOWED
            )
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response("Event(s) created successfully", status.HTTP_201_CREATED, serializer.data)

        return custom_response("Validation failed", status.HTTP_400_BAD_REQUEST, serializer.errors)

    except Exception as e:
        return custom_response(f"Internal server error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR, serializer.errors)

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

def update_booking(request, phone):
    try:
        if request.method != 'PUT':
            return custom_response(
                "Method not allowed. Allowed: PUT",
                status.HTTP_405_METHOD_NOT_ALLOWED
            )
        user = User.objects.get(phone=phone)
        booking = Booking.objects.filter(user=user).first()
        
        if not booking:
            return custom_response("No booking found for this phone", status.HTTP_404_NOT_FOUND)
        
        new_event_id = request.data.get('event')
        if new_event_id and int(new_event_id) != booking.event.id:
            new_event = Event.object.get(pk = new_event_id)

            if new_event.available_seat <= 0:
                return custom_response("No seats available", status.HTTP_404_NOT_FOUND)
            old_event = booking.event

            new_event.available_seat = F('available_seat') - 1
            new_event.save()

            old_event.available_seat = F('available_seat') + 1
            old_event.save()

            serializer = BookingSerializer(booking, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return custom_response("Booking updated successfully", status.HTTP_200_OK, serializer.data)
            else:
                new_event.available_seat = F('available_seat') + 1
                new_event.save()
                old_event.available_seat = F('available_seat') - 1
                old_event.save()
                return custom_response("Validation failed", status.HTTP_400_BAD_REQUEST, serializer.errors)
        
    except Exception as e:
        return custom_response(f"Internal server error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_event_register(request):
    user_id = request.data.get('user')
    event_id = request.data.get('event')

    try:
        if request.method != 'POST':
            return custom_response(
                "Method not allowed. Allowed: POST",
                status.HTTP_405_METHOD_NOT_ALLOWED
            )
        user = User.objects.get(pk=user_id)
        event = Event.objects.get(pk=event_id)

        if Booking.objects.filter(user=user, event=event).exists():
            return custom_response("User already registered for this event", status.HTTP_404_NOT_FOUND)

        if event.available_seat <= 0:
            return custom_response("No seats available for this event", status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(data=request.data)
        
        if serializer.is_valid():
            event.available_seat = F('available_seat') - 1
            event.save()
            
            serializer.save()
            return custom_response("Registration successful", status.HTTP_201_CREATED, serializer.data)
        
        return custom_response("Validation error",status.HTTP_400_BAD_REQUEST, serializer.errors)

    except (User.DoesNotExist, Event.DoesNotExist):
        return custom_response("User or Event not found", status.HTTP_404_NOT_FOUND)


def custom_response(message, status_code, data=None):
    return Response({
        "message": message,
        "status": status_code,
        "data": data if data is not None else {}
    }, status=status_code)

