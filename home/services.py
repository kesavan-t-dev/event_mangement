import jwt
from .models import Organiser, Event, User, Booking
from .serializers import OrganiserSerializer, EventSerializer, UserSerializer, BookingSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F
from datetime import datetime, date
from .utilities.token import generate_jwt_token
from django.conf import settings


def get_all_organisers():
    organiser_id = Organiser.objects.all()
    serializer = OrganiserSerializer(organiser_id, many=True)
    return custom_response("Organisers retrieved successfully", status.HTTP_200_OK, serializer.data)

def get_all_events():
    events_id = Event.objects.all()
    serializer = EventSerializer(events_id, many=True)
    return custom_response("Events retrieved successfully", status.HTTP_200_OK, serializer.data)

def get_all_users():
    users_id = User.objects.all()
    serializer = UserSerializer(users_id, many=True)
    return custom_response("Users retrieved successfully", status.HTTP_200_OK, serializer.data)


def event_create(request):
    if request.method != 'POST':
        return custom_response(
            f"Method {request.method} not allowed. Allowed: POST",
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    title = request.data.get('event_title')
    event_date = request.data.get('date')
    start_time = request.data.get('start_time')
    date_obj = datetime.strptime(event_date, "%Y-%m-%d").date()
    if Event.objects.filter(event_title=title, date=event_date, start_time=start_time).exists():
        return custom_response(
            f"An event is already Booked !", 
            400
        )
    if date_obj < date.today():
        return custom_response(
            "Past date is not allowed",
            400
        )

    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response("Event created successfully", 201, serializer.data)
    
    return custom_response("Validation failed", 400, serializer.errors)

    
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


def user_event_register(request):

    if request.method != 'POST':
        return custom_response(
            "Method not allowed. Allowed: POST",
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
        
    user_id = request.data.get('user_id')
    event_id = request.data.get('event_id')

    user_obj = User.objects.filter(pk=user_id).first()
    if not user_obj:
        return custom_response("User not found", 404)

    event_obj = Event.objects.filter(pk=event_id).first()
    if not event_obj:
        return custom_response("Event not found", 404)

    if Booking.objects.filter(user=user_obj, event=event_obj).exists():
        return custom_response("User already registered", 400)

    if event_obj.available_seats <= 0:
        return custom_response("No seats available", 400)

    new_booking = Booking.objects.create(
        user=user_obj, 
        event=event_obj, 
        is_active=True
    )
    
    event_obj.available_seats = F('available_seats') - 1
    event_obj.save()
    serializer = BookingSerializer(new_booking)
    
    return custom_response("Registration successful", 201, serializer.data)

def event_update(request, id):
    if request.method != 'PUT':
        return custom_response(f"Method {request.method} not allowed. Allowed: PUT", 405)

    event_instance = Event.objects.filter(pk=id).first()
    if not event_instance:
        return custom_response("Event not found", 404)

    serializer = EventSerializer(event_instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response("Event updated successfully", 200, serializer.data)
    
    return custom_response("Validation failed", 400, serializer.errors)


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

def login(request):
    email = request.data.get('username')
    password = request.data.get('password')

    account = User.objects.filter(email=email, password=password).first()
    account_type = "user"
    serializer_class = UserSerializer

    if not account:
        account = Organiser.objects.filter(email=email, password=password).first()
        account_type = "organiser"
        serializer_class = OrganiserSerializer

    if not account:
        return custom_response("Invalid Credentials", 401)

    token = generate_jwt_token(account, account_type)

    account_data = serializer_class(account).data

    return custom_response("Login Successful", 200, {
        'token': token,
        'account_type': account_type,
        'user_details': account_data
    })


def refresh_access_token(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return custom_response("Refresh token is required", 400)
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        account_type = payload.get('type')
        if account_type == "user":
            account = User.objects.filter(pk=user_id).first()
        else:
            account = Organiser.objects.filter(pk=user_id).first()
        if not account:
            return custom_response("Account no longer exists", 404)
        now = datetime.datetime.utcnow()
        new_access_payload = {
            'user_id': user_id,
            'type': account_type,
            'exp': now + datetime.timedelta(hours=1),
            'iat': now,
        }
        new_access_token = jwt.encode(new_access_payload, settings.SECRET_KEY, algorithm='HS256')
        return custom_response("Token refreshed", 200, {'access': new_access_token})
    except jwt.ExpiredSignatureError:
        return custom_response("Refresh token expired. Please login again.", 401)
    except jwt.InvalidTokenError:
        return custom_response("Invalid refresh token", 401)

def custom_response(message, status_code, data=None):
    return Response({
        "message": message,
        "status": status_code,
        "data": data if data is not None else {}
    }, status=status_code)

