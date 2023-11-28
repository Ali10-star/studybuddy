# Django Rest Framework imports
from rest_framework.serializers import ModelSerializer

# App imports
from base.models import User, Room

class RoomSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

