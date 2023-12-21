from .models import Topic, Room, Message, ProfilePic
from .forms import TopicForm, RoomForm, MessageForm, UserForm, ProfilePicForm

from django.db.models import Count, Q
from django.shortcuts import render, redirect

from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

# Takes a request and gives a response
# Essentially a request handler

# Funtion takes a request object and returns a response
def home_page(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
        )
    topics = Topic.objects.all()
    topicsWithCount = topics.annotate(room_count=Count('room'))
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')
    # Use Render to return html files. 
    # It automatically checks the template folder
    # First Parameter: always request, Second: html file, Third, variable dictionary
    return render(request, 'playground/home.html', { 'title': 'Home Page', 'rooms': rooms, 'topics': topicsWithCount, 'room_messages': room_messages[:5]})

def topics_page(request):
    topics = Topic.objects.all()
    topicsWithCount = topics.annotate(room_count=Count('room'))
    rooms = Room.objects.all()
    return render(request, 'playground/topics.html', { 'title': 'Home Page', 'rooms': rooms, 'topics': topicsWithCount} )

def activity_page(request):
    room_messages = Message.objects.all().order_by('-created')
    return render(request, 'playground/activity.html', { 'title': 'Home Page', 'room_messages': room_messages[:5] } )

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.error(request, 'Already Logged In')
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'No User Exists')
        user = authenticate(request, username=username, password=password)
        if user != None: 
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')
    context = {'page': page}
    return render(request, 'playground/register_login.html', context)

@login_required(login_url='login')
def logout_user(request):
    logout(request) 
    return redirect('home')

def register_page(request):
    page = 'register'
    form = UserCreationForm()
    if request.user.is_authenticated:
        messages.error(request, 'Already Logged In')
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            ProfilePic.objects.create(user=user)
            return redirect('home')
        else:
            messages.error(request, 'Error Occured Durning Registration')
    context = {'page': page, 'form': form }
    return render(request, 'playground/register_login.html', context)

def profile(request, pk):
    user = User.objects.get(id=pk)
    profile_pic = ProfilePic.objects.get(user=user)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    topicsWithCount = topics.annotate(room_count=Count('room'))
    context = {"profile_user" : user, 'rooms': rooms, 'room_messages': room_messages[:5], 'topics': topicsWithCount, 'profile_pic': profile_pic}
    return render(request, 'playground/profile.html', context)

@login_required(login_url='login')
def update_profile(request):
    user = request.user
    profile_pic = ProfilePic.objects.get(user=user)
    user_form = UserForm(instance=user)
    profile_pic_form = ProfilePicForm(instance=profile_pic)
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=user)
        profile_pic_form = ProfilePicForm(request.POST, request.FILES, instance=profile_pic)
        if user_form.is_valid() and profile_pic_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            profile_pic_form.save()
            return redirect('profile', request.user.id)

    context = {'user_form': user_form, 'profile_pic_form': profile_pic_form}
    return render(request, 'playground/update_profile.html', context)

def room_page(request, pk):
    room = Room.objects.get(id=pk)
    comments = Message.objects.filter(room=room).order_by('-created')
    partcipants = room.partcipants.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            body = request.POST.get('body')
            message = Message.objects.create(
                user = request.user,
                room = room,
                body = body
            )
            room.partcipants.add(request.user)
            message.save()
            return redirect('room', pk=room.id)
        else:
            messages.error(request, 'Need to be logged in')
    context = { 'room': room, 'comments': comments, 'partcipants': partcipants }
    return render(request, 'playground/room.html', context )

@login_required(login_url='login')
def room_form(request):
    page = 'create_room'
    topics = Topic.objects.all()
    if request.method == 'POST': 
        if request.POST.get('topic') != None and request.POST.get('name') != "":
            room = Room.objects.create(
                host = request.user,
                topic = Topic.objects.get(id=request.POST.get('topic')),
                name = request.POST.get('name'),
                description = request.POST.get('description')
            )
            return redirect('home')
        else:
            messages.error(request, "An Error Occured")
        
    context = {'topics': topics, 'page': page}
    return render(request, 'playground/room_form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    page = 'update_room'
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        messages.error(request, 'Access Denied')
        return redirect('home')
    if request.method == 'POST': 
        if request.POST.get('name') != "":
            room.name = request.POST.get('name')
            room.description = request.POST.get('description')
            room.save()
            return redirect('home')
        else:
            messages.error(request, "An Error Occured")
    context = {'room': room, 'page': page}
    return render(request, 'playground/room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        messages.error(request, 'Access Denied')
        return redirect('home')
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, "playground/delete.html", {'obj': room})

@login_required(login_url='login')
def update_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        messages.error(request, 'Access Denied')
        return redirect('home')
    if request.method == 'POST': 
        if request.POST.get('') != "":
            message.body = request.POST.get('body')
            message.save()
        else:
            messages.error(request, "An error occured")
        return redirect('home')

    context = {'message': message }
    return render(request, 'playground/message_form.html', context)

@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        messages.error(request, 'Access Denied')
        return redirect('home')
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, "playground/delete.html", {'obj': message})

def topic_form(request):
    form = TopicForm()
    if request.method == 'POST': 
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request, "An Error Occured")
    context = {'form': form}
    return render(request, 'playground/topic_form.html', context)

def update_topic(request, pk):
    topic = Topic.objects.get(id=pk)
    form = TopicForm(instance=topic)
    if request.method == 'POST': 
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request, "An Error Occured")
    context = {'form': form}
    return render(request, 'playground/topic_form.html', context)

def delete_topic(request, pk):
    topic = Topic.objects.get(id=pk)
    if request.method == "POST":
        topic.delete()
        return redirect('home')
    return render(request, "playground/delete.html", {'obj': topic})