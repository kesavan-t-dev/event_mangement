from django.urls import path
from . import views


urlpatterns = [
    path('list_organiser/', views.organiser_list, name='organiser_list'),
    path('create_event/', views.event_create, name='event_create'),
]