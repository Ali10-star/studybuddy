from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import django.contrib.auth as django_auth

from .models import User, Room, Topic, Message
from .forms import RoomForm, UserUpdateForm, CustomCreationForm

# Create your views here.

def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist!')

        user = django_auth.authenticate(request, email=email, password=password)

        if user:
            django_auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist!')


    context = {'page': page}
    return render(request, template_name='base/login_register.html', context=context)


def logout_user(request):
    django_auth.logout(request)
    return redirect('home')


def register_user(request):
    form = CustomCreationForm()

    if request.method == 'POST':
        form = CustomCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            django_auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')

    context = {'form': form}
    return render(request, template_name='base/login_register.html', context=context)


def home(request):
    query = request.GET.get('q')
    if query:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=query) |
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        room_messages = Message.objects.filter(Q(room__topic__name__icontains=query))
    else:
        rooms = Room.objects.all()
        room_messages = Message.objects.all()

    room_count = str(rooms.count())
    topics = Topic.objects.all()

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count,
               'room_messages': room_messages}

    return render(request, template_name='base/home.html', context=context)


def view_room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.messages.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('comment-body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': messages, 'participants': participants}
    return render(request, template_name='base/room.html', context=context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, template_name='base/room_form.html', context=context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You're not allowed to edit a room that isn't yours.")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description=request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, template_name='base/room_form.html', context=context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=int(pk))
    obj_type = room.__class__.__name__

    if request.user != room.host:
        return HttpResponse("You're not allowed to delete a room that isn't yours.")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room, 'obj_type': obj_type}
    return render(request, template_name='base/components/delete.html', context=context)

# ----------------- MESSAGES ----------------------
@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=int(pk))
    obj_type = message.__class__.__name__
    room_id = message.room.id

    if request.user != message.user:
        return HttpResponse("You cannot delete a comment that wasn't posted by you.")

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=room_id)

    context = {'obj': message, 'obj_type': obj_type}
    return render(request, template_name='base/components/delete.html', context=context)

# ----------------- PROFILE ----------------------
@login_required(login_url='login')
def user_profile(request, pk):
    viewed_user = User.objects.get(id=int(pk))
    user_rooms = viewed_user.hosted_rooms.all()
    topics = {room.topic for room in user_rooms}
    user_messages = viewed_user.sent_messages.all()

    context = {'viewed_user': viewed_user,
               'user_rooms': user_rooms,
               'topics': topics,
               'room_messages': user_messages}
    return render(request, template_name='base/profile.html', context=context)


@login_required(login_url='login')
def update_profile(request):
    user = request.user
    form = UserUpdateForm(instance=user)

    if request.method == 'POST':
        form = UserUpdateForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}
    return render(request, template_name='base/update-user.html', context=context)

# ----------------- TOPICS ----------------------

def view_topics(request):
    query = request.GET.get('q')

    if query:
        topics = Topic.objects.filter(
            Q(name__icontains=query)
        )
    else:
        topics = Topic.objects.all()

    context = {'topics': topics}
    return render(request, template_name='base/topics.html', context=context)


def view_recent_activities(request):
    recent = Message.objects.all()[:3]

    context = {'recent_messages': recent}
    return render(request, template_name='base/activity.html', context=context)