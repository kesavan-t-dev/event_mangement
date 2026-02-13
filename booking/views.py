from rest_framework.decorators import api_view
from . import services

@api_view(['POST'])
def user_event_register(request):
    return services.user_event_register(request)