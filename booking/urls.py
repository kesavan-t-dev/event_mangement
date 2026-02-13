from django.urls import path
from . import views


urlpatterns = [    
    path('event_register/', views.user_event_register, name='user_event_register'),
]