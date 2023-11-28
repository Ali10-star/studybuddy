from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('room/<str:pk>', views.view_room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<str:pk>', views.update_room, name='update-room'),
    path('delete-room/<str:pk>', views.delete_room, name='delete-room'),

    path('topics/', views.view_topics, name='topics'),
    path('activities/', views.view_recent_activities, name='activities'),

    path('profile/<str:pk>', views.user_profile, name='user-profile'),
    path('update-user/', views.update_profile, name='update-user'),

    path('delete-message/<str:pk>', views.delete_message, name='delete-message'),
]
