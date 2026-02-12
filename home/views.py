from rest_framework.decorators import api_view
from . import services

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class RestrictedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data={"message": "You have access to this restricted content."})

@api_view(['GET'])
def organiser_list(request):
    return services.get_all_organisers()

@api_view(['GET'])
def event_list(request):
    return services.get_all_events()

@api_view(['GET'])
def user_list(request):
    return services.get_all_users()

@api_view(['POST'])
def event_create(request):
    return services.event_create(request)

@api_view(['POST'])
def user_create(request):
    return services.user_create(request)

@api_view(['POST'])
def user_event_register(request):
    return services.user_event_register(request)

@api_view(['PUT'])
def event_update(request, id):
    return services.event_update(request, id)

@api_view(['PATCH'])
def user_update(request, id):
    return services.user_update(request, id)

@api_view(['POST'])
def login_api(request):
    return services.login(request)

@api_view(['GET'])
def my_subscription(request):
    return services.my_events(request)
