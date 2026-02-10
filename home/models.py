import uuid
from django.db import models

class Organiser(models.Model):
    Organiser_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=150, unique=True)
    updated_at = models.DateTimeField(auto_now=True)   
    created_at = models.DateTimeField(auto_now_add=True)  
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "organiser" 

class User(models.Model):
    User_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=150, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "user"  

class Event(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    organisers = models.ForeignKey(Organiser, on_delete=models.CASCADE, db_column="org_id")
    event_title = models.CharField(max_length=150)
    event_type = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=300)
    available_seat = models.IntegerField()
    total_seats = models.IntegerField()
    start_time = models.TimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "event"  


class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column="event")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "booking"  
        unique_together = ('user', 'event')  

