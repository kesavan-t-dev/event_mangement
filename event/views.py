from rest_framework.decorators import api_view
from . import services

@api_view(['GET'])
def event_list(request):
    return services.get_all_events()

