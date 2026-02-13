from .models import User
from django.db.models import F
from .serializers import UserSerializer
from booking.serializers import BookingSerializer
from rest_framework import status
from utilities.custom import custom_response
from event.models import Event
from booking.models import Booking
from datetime import date
from utilities.authentication import verify_token

def get_all_users():
    users_id = User.objects.all()
    serializer = UserSerializer(users_id, many=True)
    return custom_response("Users retrieved successfully", status.HTTP_200_OK, serializer.data)


def user_create(request):
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

def user_update(request, id):
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


def my_events(request):

    auth_user, error_response = verify_token(request)
    if error_response:
        return error_response

    if auth_user.account_type != "user":
        return custom_response("Access Denied", 403)

    my_bookings = Booking.objects.filter(
        user_id=auth_user.user_id, 
        is_active=True
    ).select_related('event')
    
    serializer = BookingSerializer(my_bookings, many=True)
    
    return custom_response("My Subscriptions", 200, serializer.data)


