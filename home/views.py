from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import services


@api_view(['GET'])
def organiser_list(request):
    data = services.get_all_organisers()
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def event_list(request):
    data = services.get_all_events()
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_list(request):
    data = services.get_all_users()
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def booking_list(request):
    data = services.get_all_bookings()
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def update_organiser(request):
    result = services.update_organiser(request.data)
    return Response(result)

@api_view(['POST'])
def event_create(request):
    event = services.event_create(request.data)
    return Response(event)

@api_view(['POST'])
def user_create(request):
    user = services.user_create(request.data)
    return Response(user)

@api_view(["POST"])
def booking_update(request, pk):
    booking = services.update_booking(request, pk)
    return Response(booking)