from django.forms import ModelForm
from .models import User, Room
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class CustomCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio', 'avatar']