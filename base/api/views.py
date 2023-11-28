# Django Rest Framework imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# App imports
from base.models import User, Room
from .serializers import RoomSerializer, UserSerializer


@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/users',
        'GET /api/rooms/:id',
    ]

    return Response(data=routes, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    room_serializer = RoomSerializer(rooms, many=True)
    return Response(room_serializer.data)


@api_view(['GET'])
def get_room(request, pk):
    room = Room.objects.get(id=int(pk))
    room_serializer = RoomSerializer(room)
    return Response(room_serializer.data)



@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    user_serializer = UserSerializer(users, many=True)
    return Response(user_serializer.data)