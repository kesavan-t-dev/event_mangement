import uuid
from django.db import models
from user.models import User
from event.models import Event
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