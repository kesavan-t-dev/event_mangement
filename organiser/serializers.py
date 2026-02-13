from rest_framework import serializers
from .models import Organiser

class OrganiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organiser
        fields = ['organiser_id','name','phone','email']