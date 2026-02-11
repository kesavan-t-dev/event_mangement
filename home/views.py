from rest_framework.decorators import api_view
from . import services

@api_view(['GET'])
def organiser_list(request):
    # Returns the custom_response directly from services
    return services.get_all_organisers()

@api_view(['GET'])
def event_list(request):
    return services.get_all_events()

@api_view(['GET'])
def user_list(request):
    return services.get_all_users()

@api_view(['GET'])
def booking_list(request):
    return services.get_all_bookings()

@api_view(['PATCH'])
def update_organiser(request, phone): 
    return services.update_organiser(request, phone)

@api_view(['POST'])
def event_create(request):
    return services.event_create(request)

@api_view(['POST'])
def user_create(request):
    return services.user_create(request)

@api_view(["PUT"])
def booking_update(request, phone):
    return services.update_booking(request, phone)
