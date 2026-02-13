from rest_framework.decorators import api_view
from . import services


@api_view(['GET'])
def organiser_list(request):
    return services.get_all_organisers()

@api_view(['POST'])
def event_create(request):
    return services.event_create(request)



