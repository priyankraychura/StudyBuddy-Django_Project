from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_datetime
# from django.contrib.auth.forms import UserCreationForm

from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
import random
from django.core.mail import send_mail

# from django.urls import reverse

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me!'},
#     {'id': 3, 'name': 'Fronend developers'},
# ]

# Create your views here.
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        isAdmin = request.POST.get('isAdmin')

        try:
            user = User.objects.get(email=email)
        except:
            pass

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            if isAdmin:
                if user.is_staff:
                    return redirect('dashboard')
                else:
                    messages.error(request, 'You don\'t have the admin rights! Logged in as normal user.')

            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exists')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration!')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) 
        )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
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
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance=room)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    room = message.room  # Get the room associated with the message

    if request.user != message.user and not request.user.is_staff:
        return HttpResponse('Your are not allowed here!!')
    
    if request.method == 'POST':
        # Check if the user has any other messages in the room
        other_messages = Message.objects.filter(room=room, user=message.user).exclude(id=pk)

        # If no other messages by the user, remove the user from participants
        if not other_messages.exists():
            print(request.user)
            room.participants.remove(message.user)    
    
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activitiyPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

def forgotPass(request):
    session_otp = request.session.get('otp')
    session_expiration_time = request.session.get('otp_expiration')
    email = request.session.get('reset_email')
    
    if session_otp and session_expiration_time and email:
        expiration_time = parse_datetime(session_expiration_time)
        if timezone.now() < expiration_time:
            return redirect('varifyOTP')

    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            try:
                user = User.objects.get(email = email)
                OTP = random.randint(100000, 999999)
                expiration_time = timezone.now() + timedelta(minutes=10)
                print("User exists: ",email, OTP)

                request.session['otp'] = OTP
                request.session['otp_expiration'] = expiration_time.isoformat()
                request.session['reset_email'] = email

                try:
                    send_mail(
                        'Rest Password',
                        f'Your OTP is: {OTP}' ,
                        'priyankraychura.online@gmail.com',
                        [f'{email}'],
                        fail_silently=False
                    )

                    messages.success(request, f'A verification code has been sent to your email! -> {OTP}')
                    
                except:
                    messages.success(request, f'A verification code has been sent to your email! -> {OTP}')

                return redirect("varifyOTP")

            except User.DoesNotExist:
                print("User do not exist")
                return redirect("home") 

    return render(request, "base/forgotPass.html")

def varifyOTP(request):
    session_verification_code = request.session.get('otp')
    session_expiration_time = request.session.get('otp_expiration')
    
    if not session_verification_code or not session_expiration_time:
        return redirect('forgotPass')

    if request.method == "POST":
        # session_verification_code = request.session.get('otp')
        # session_expiration_time = request.session.get('otp_expiration')
        email = request.session.get('reset_email')
        verification_code = request.POST.get('otp')

        print(type(session_verification_code))
        print("OTP Expire: ", session_expiration_time)

        # email = request.session.get('reset_email')
        if verification_code and session_verification_code and email:
            expiration_time = parse_datetime(session_expiration_time)
            print("New Expire time: ", expiration_time)
            print(timezone.now() <= expiration_time)
            if timezone.now() <= expiration_time:
                if int(verification_code) == session_verification_code:
                    messages.success(request, 'OTP has varified successfully!')

                    del request.session['otp']
                    del request.session['otp_expiration']

                    return redirect("resetPass")
                else:
                    messages.error(request, 'Invalid OTP.')
            else:
                messages.error(request, 'Invalid or expired verification code')
                return redirect('forgotPass')
        else:
            messages.error(request, 'OTP field should not be empty.')

    return render(request, "base/varifyOTP.html")

def resendOTP(request):
    session_otp = request.session.get('otp')
    session_expiration_time = request.session.get('otp_expiration')
    email = request.session.get('reset_email')

    if not session_otp and not session_expiration_time and not email:
        return redirect('forgotPass')

    OTP = random.randint(100000, 999999)
    expiration_time = timezone.now() + timedelta(minutes=10)

    print("New OTP: ", OTP)

    request.session['otp'] = OTP
    request.session['otp_expiration'] = expiration_time.isoformat()

    try:
        send_mail(
            'Rest Password',
            f'Your OTP is: {OTP}' ,
            'priyankraychura.online@gmail.com',
            [f'{email}'],
            fail_silently=False
        )

        messages.success(request, f'A verification code has been sent to your email! -> {OTP}')
        
    except:
        messages.success(request, f'A verification code has been sent to your email! -> {OTP}')

    return redirect("varifyOTP")

def resetPass(request):
    email = request.session.get('reset_email')

    print(email)

    if not email:
        return redirect('forgotPass')

    if request.method == "POST":
        newPass = request.POST.get('newPass')
        cnfPass = request.POST.get('cnfPass')

        print(newPass)

        if newPass == cnfPass:
            
            user = User.objects.get(email=email)
            user.set_password(newPass)
            user.save()

            del request.session['reset_email']

            return redirect("login")
        else:
            messages.error(request, 'Password and Confirm Password should match.')

    return render(request, "base/resetPass.html")

@login_required(login_url='login')
def like_item(request, item_id):

    if not request.user.is_authenticated:
        return JsonResponse({'authenticated': False})
    
    item = get_object_or_404(Room, id=item_id)
    
    print(item)
    if request.user in item.likes.all():    
        item.likes.remove(request.user)
        liked = False
    else:
        item.likes.add(request.user)
        liked = True

    print(item.likes.count())
    return JsonResponse({'likes_count': item.likes.count(), 'liked': liked, 'authenticated': True})
