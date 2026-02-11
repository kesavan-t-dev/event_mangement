from django.urls import path
from . import views

urlpatterns = [
    path('organiser_list/', views.organiser_list, name='organiser_list'),
    path('event_list/', views.event_list, name='event_list'),
    path('user_list/', views.user_list, name='user_list'),
    path('event_create/', views.event_create, name='event_create'),
    path('user_create/', views.user_create, name='user_create'),
    path('user_event_register/', views.user_event_register, name='user_event_register'),
    path('event_update/<uuid:id>/', views.event_update, name='event-update'),
    path('user_update/<uuid:id>/', views.user_update, name='user-update'),  
]
