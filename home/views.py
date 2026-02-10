from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import services

def custom_response(message, status_code, instance, exclude_fields=None):
    data = {}
    for field, value in instance.items():
        if exclude_fields and field in exclude_fields:
            continue
        data[field] = value
    return Response({
        "message": message,
        "status": status_code,
        "properties": data
    }, status=status_code)


@api_view(['GET'])
def organiser_list(request):
    data = services.get_all_organisers()
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def organiser_create(request):
    result, errors = services.create_organiser(request.data)
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    return custom_response(
        "organiser created successfully",
        status.HTTP_201_CREATED,
        result,
        exclude_fields=['created_at', 'updated_at', 'is_active']
    )


@api_view(['GET'])
def event_list(request):
    data = services.get_all_events()
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def event_create(request):
    result, errors = services.create_event(request.data)
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    return custom_response(
        "event created successfully",
        status.HTTP_201_CREATED,
        result,
        exclude_fields=['created_at', 'updated_at', 'is_active']
    )


@api_view(['GET'])
def user_list(request):
    data = services.get_all_users()
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def user_create(request):
    result, errors = services.create_user(request.data)
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    return custom_response(
        "user created successfully",
        status.HTTP_201_CREATED,
        result,
        exclude_fields=['created_at', 'updated_at', 'is_active']
    )


@api_view(['POST'])
def user_event_register(request):
    result, errors = services.register_user_for_event(request.data)
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    return custom_response(
        "user registered for event successfully",
        status.HTTP_201_CREATED,
        result,
        exclude_fields=['created_at', 'updated_at', 'is_active']
    )


@api_view(['GET'])
def booking_list(request):
    data = services.get_all_bookings()
    return Response(data, status=status.HTTP_200_OK)
