from django.http import HttpResponse
from django.shortcuts import redirect, render
# from django.contrib.auth import update_session_auth_hash
from base.forms import RoomForm, UserAdminForm
from base.models import *
from django.db.models import Q, Count
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import Lower
# from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .dashboardData import *

# Create your views here.
def is_staff_user(user):
    return user.is_staff

def temp(request):
    return render(request, 'adminPanel/temp.html')

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def logoutAdmin(request):
    logout(request)

    return redirect('login')

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def deleteRoom(request, delId):
    room = Room.objects.get(id=delId)

    if request.method == "GET":
        room.delete()

        return redirect('manageRooms')

    return redirect('manageRooms')

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    topic_name = request.POST.get('topic')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # form = RoomForm(request.POST, instance=room)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('manageRooms')

    return render(request, 'adminPanel/manageRooms.html')

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def manageRooms(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    likes = request.GET.get('likes')
    participents = request.GET.get('participents')

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(host__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) 
    )

    # Apply the boolean filters only if they are checked (not None)
    if likes:
        rooms = Room.objects.annotate(
            num_likes=Count('likes'),
        ).filter(num_likes=0)
    if participents:
        rooms = Room.objects.annotate(
            num_participants=Count('participants')
        ).filter(num_participants=0)
    
    order = Lower(request.GET.get('order')) if request.GET.get('order') != None else 'id'
    rooms = rooms.order_by(order)

    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}

    return render(request, 'adminPanel/manageRooms.html', context)

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def insertRoom(request):
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
        return redirect('manageRooms')

    context = {'form': form, 'topics': topics}
    return render(request, 'adminPanel/insertRoom.html', context)

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def manageUsers(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    is_active = request.GET.get('is_active')
    is_staff = request.GET.get('is_staff')
    is_superuser = request.GET.get('is_superuser')

    users = User.objects.all().filter(
        Q(name__icontains = q) |
        Q(username__icontains = q) |
        Q(email__icontains = q) |
        Q(bio__icontains = q)
    )

    # Apply the boolean filters only if they are checked (not None)
    if is_active:
        users = users.filter(is_active=True)
    if is_staff:
        users = users.filter(is_staff=True)
    if is_superuser:
        users = users.filter(is_superuser=True)

    # Order results if needed (for example, by username)
    order = request.GET.get('order') if request.GET.get('order') != None else 'id'
    users = users.order_by(order)

    context = {'users': users}

    return render(request, 'adminPanel/manageUsers.html', context)

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def insertUser(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        username = request.POST.get('username')
        bio = request.POST.get('bio')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_active = request.POST.get('is_active') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        # Handle file upload for avatar
        avatar = request.FILES['avatar'] if 'avatar' in request.FILES else None

        # print(password == request.POST.get('cnfPassword'))
        if password == request.POST.get('cnfPassword'):
            # Create a new user
            user = User.objects.create(
                name=name,
                username=username,
                bio=bio,
                email=email,
                is_active=is_active,
                is_staff=is_staff,
                is_superuser=is_superuser,
            )

            if avatar:
                user.avatar = avatar

            # Set password
            user.set_password(password)

            # Save the user to the database
            user.save()

            # Redirect to a success page or back to the form
            return redirect('manageUsers')
        else:
            return HttpResponse('Password and confirm password does not match')

    return render(request, "adminPanel/insertuser.html")

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def updateUser(request, pk):
    print("called")
    user = User.objects.get(id = pk)
    form = UserAdminForm(instance=user)

    if request.method == 'POST':
        # form = RoomForm(request.POST, instance=room)
        user.name = request.POST.get('name')
        user.username = request.POST.get('username')
        # user.is_active = request.POST.get('username')
        
        is_active = request.POST.get('active', False)
        user.is_active = True if is_active else False

        user.email = request.POST.get('email')
        user.bio = request.POST.get('bio')
        # user.set_password(request.POST.get('password'))
        user.save()
        # update_session_auth_hash(request, user)
        return redirect('manageUsers')

    return render(request, 'adminPanel/manageUsers.html')

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def deleteUser(request, delId):
    user = User.objects.get(id=delId)

    if request.method == "GET":
        user.delete()

        return redirect('manageUsers')

    return redirect('manageUsers')

from django.shortcuts import get_object_or_404

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def insertTopic(request):
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic_id = request.POST.get('topic_id')

        if topic_id:  # If an ID is provided, update the existing topic
            topic = get_object_or_404(Topic, id=topic_id)
            topic.name = topic_name
            topic.save()
        else:  # If no ID, create a new topic
            Topic.objects.create(name=topic_name)

    return redirect('manageTopics')

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def manageTopics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.all().filter(
        Q(name__icontains = q)
    )

    rooms = Room.objects.all()

    order = Lower(request.GET.get('order')) if request.GET.get('order') != None else 'id'
    topics = topics.order_by(order)

    context = {'topics': topics, 'rooms': rooms}


    return render(request, 'adminPanel/manageTopics.html', context)

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def deleteTopic(request, delId):
    topic = Topic.objects.get(id=delId)

    if request.method == "GET":
        topic.delete()

        return redirect('manageTopics')

    return redirect('manageTopics')

@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def dashboard(request):
    query = request.GET.get('q', '')

    if query:
        return redirect(f'/adminPanel/manageUsers/?q={query}')

    users = get_all_users()
    rooms = get_all_rooms()
    staff = get_staff(True)
    active = get_top_5_users_by_participation()
    popularRooms = get_top_5_rooms()

    # Getting counts
    user_count = get_user_count()
    user_count -= 1
    room_count = get_room_count()
    room_count -= 1
    message_count = get_message_count()
    message_count -= 1
    topic_count = get_topic_count()
    topic_count -= 1
    table_count = get_table_count()

    # Getting database info
    db_status = check_database_status()
    db_integrity = check_db_integrity()
    db_size = get_database_size()
    tables_list = list_tables()

    context = {
        'users': users, 
        'rooms': rooms, 
        'staff': staff, 
        'popularRooms': popularRooms,
        'user_count': user_count, 
        'room_count': room_count, 
        'message_count': message_count, 
        'topic_count': topic_count, 
        'table_count': table_count, 
        'db_status': db_status,
        'db_integrity': db_integrity, 
        'db_size': db_size, 
        'tables_list': tables_list
        }



    return render(request, "adminPanel/dashboard.html", context)