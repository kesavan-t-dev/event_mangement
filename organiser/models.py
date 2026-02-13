import uuid
from django.db import models

class Organiser(models.Model):
    organiser_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128) 
    updated_at = models.DateTimeField(auto_now=True)   
    created_at = models.DateTimeField(auto_now_add=True)  
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "organiser" 
