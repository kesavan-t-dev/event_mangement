from .models import Organiser, Event, User, Booking
from .serializers import OrganiserSerializer, EventSerializer, UserSerializer, BookingSerializer
from rest_framework import status
from rest_framework.response import Response

def get_all_organisers():
    return  OrganiserSerializer(Organiser.objects.all(), many=True).data

def get_all_events():
    return EventSerializer(Event.objects.all(), many=True).data

def get_all_users():
    return UserSerializer(User.objects.all(), many=True).data


def update_organiser(request, pk):
    try:
        if request.method != 'PATCH':
            return custom_response(
                f"Method {request.method} not allowed. Allowed: PATCH",
                status.HTTP_405_METHOD_NOT_ALLOWED
            )

        organiser = Organiser.objects.get(pk=pk)

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
        return custom_response(f"Internal server error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        return custom_response(f"Internal server error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

def update_booking(request, pk):
    try:
        if request.method != 'PUT':
            return custom_response(
                f"Method {request.method} not allowed. Allowed: PUT",
                status.HTTP_405_METHOD_NOT_ALLOWED
            )

        booking = Booking.objects.get(pk=pk)

        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                "Booking updated successfully (PUT)",
                status.HTTP_200_OK,
                serializer.data
            )

        return custom_response("Validation failed", status.HTTP_400_BAD_REQUEST, serializer.errors)

    except Booking.DoesNotExist:
        return custom_response("Booking not found", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return custom_response(f"Internal server error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)



def custom_response(message, status_code, data=None):
    return Response({
        "message": message,
        "status": status_code,
        "data": data if data is not None else {}
    }, status=status_code)

