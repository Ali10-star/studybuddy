from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes, name='get-routes'),
    path('rooms/', views.get_rooms, name='get-rooms'),
    path('users/', views.get_users, name='get-users'),
    path('rooms/<str:pk>', views.get_room, name='get-room'),
]