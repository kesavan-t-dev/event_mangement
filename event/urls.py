from django.urls import path
from . import views


urlpatterns = [
    path('list_event/', views.event_list, name='event_list'),
]