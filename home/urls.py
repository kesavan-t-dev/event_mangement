from django.urls import path
from . import views

urlpatterns = [
    path('organiser_list/', views.organiser_list, name='organiser_list'),
    path('event_create/', views.event_create, name='event_create'),
    path('event_list/', views.event_list, name='event_list'),
    path('user_create/', views.user_create, name='user_create'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_event_register/', views.user_event_register, name='user_event_register'),
    path('booking_list/', views.booking_list, name='booking_list'),  
    path('organiser_create/', views.organiser_create, name='organiser_create'),  
]
