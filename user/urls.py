from django.urls import path
from . import views


urlpatterns = [
    path('list_user/', views.user_list, name='user_list'),
    path('update_user/<uuid:id>/', views.user_update, name='user_update'),
    path('create_user/', views.user_create, name='user_create'),
    path('my_events/', views.my_subscription, name='my_events'),
]