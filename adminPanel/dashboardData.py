from base.models import User, Room, Message, Topic
from django.db import connection
import os
from django.conf import settings
from django.db.models import Count

def get_all_users():
    return User.objects.all()

def get_staff(check):
    return User.objects.filter(is_staff=check)

def get_all_rooms():
    return Room.objects.filter()

def get_message_count():
    return Message.objects.count()

def get_room_count():
    return Room.objects.count()

def get_user_count():
    return User.objects.count()

def get_topic_count():
    return Topic.objects.count()

from django.db.models import Count

def get_top_5_rooms():
    return Room.objects.annotate(participant_count=Count('participants')).order_by('-participant_count')[:5]

def get_top_5_users_by_participation():
    # Aggregate users by counting their participation in rooms
    top_users = User.objects.annotate(
        participation_count=Count('room')  # Adjust 'room' to the correct related name
    ).order_by('-participation_count')[:5]
    
    return top_users


def check_database_status():
    return connection.is_usable()

def check_db_integrity():
    cursor = connection.cursor()
    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()
    return result[0] == "OK"


def get_database_size():
    db_path = settings.DATABASES['default']['NAME']
    if os.path.exists(db_path):
        size_in_mb = os.path.getsize(db_path) / (1024 * 1024)
        return size_in_mb
    return "Database file not found."

def get_table_count():
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Filter tables that belong to the 'base' app
    base_tables = [table[0] for table in tables if table[0].startswith('base_')]
    
    return len(base_tables)


def list_tables():
    with connection.cursor() as cursor:
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Filter tables that belong to the 'base' app
        base_tables = [table[0] for table in tables if table[0].startswith('base_')]
        
        table_sizes = []
        for table_name in base_tables:
            # Get the number of rows in the table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]
            
            # Estimate the size per row by counting columns and assuming a fixed size per column
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            column_count = len(columns)
            
            # Estimate size per row (this is a rough estimate, you can adjust the size factor)
            size_per_row = column_count * 100  # assuming 100 bytes per column as an estimate
            
            # Estimate the total table size
            table_size = (row_count * size_per_row) / 1024
            
            # Store the table name and size as a tuple
            table_sizes.append((table_name, table_size))
        
        if table_sizes:
            return table_sizes
        else:
            return False

