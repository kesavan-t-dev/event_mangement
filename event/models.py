import uuid
from django.db import models
from organiser.models import Organiser

class Event(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    organisers_id = models.ForeignKey(Organiser, on_delete=models.CASCADE, db_column="org_id")
    event_title = models.CharField(max_length=150)
    event_type = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=300)
    available_seats = models.IntegerField()
    total_seats = models.IntegerField()
    start_time = models.TimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "event"  
