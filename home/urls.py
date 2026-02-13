from django.urls import path
from . import views


urlpatterns = [
    path('list_organiser/', views.organiser_list, name='organiser_list'),
    path('list_event/', views.event_list, name='event_list'),
    path('list_user/', views.user_list, name='user_list'),
    path('create_event/', views.event_create, name='event_create'),
    path('create_user/', views.user_create, name='user_create'),
    path('event_register/', views.user_event_register, name='user_event_register'),
    path('update_event/<uuid:id>/', views.event_update, name='event_update'),
    path('update_user/<uuid:id>/', views.user_update, name='user_update'), 
    path('login/',views.login_api, name='login'),
    # path('my_events/', views.my_subscription, name='my_events'),
    path('refresh_token/', views.refresh_token, name='refresh-token'),


]
