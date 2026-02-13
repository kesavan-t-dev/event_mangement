from rest_framework.decorators import api_view
from . import services

@api_view(['GET'])
def user_list(request):
    return services.get_all_users()
@api_view(['POST'])
def user_create(request):
    return services.user_create(request)

@api_view(['PATCH'])
def user_update(request, id):
    return services.user_update(request, id)

@api_view(['GET'])
def my_subscription(request):
    return services.my_events(request)


