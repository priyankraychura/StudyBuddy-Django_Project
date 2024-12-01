from django.urls import path
from . import views

urlpatterns = [
    # path('', views.mainPanel, name = "mainPanel"),
    path('', views.dashboard, name = "dashboard"),
    path('temp/', views.temp, name = "temp"),
    path('logoutAdmin/', views.logoutAdmin, name = "logoutAdmin"),
    path('manageRooms/', views.manageRooms, name = "manageRooms"),
    path('insertRoom/', views.insertRoom, name = "insertRoom"),
    path('insertUser/', views.insertUser, name = "insertUser"),
    path('manageUsers/', views.manageUsers, name = "manageUsers"),
    path('deleteRoom/<delId>', views.deleteRoom, name = "deleteRoom"),
    path('updateRoom/<pk>', views.updateRoom, name = "updateRoom"),
    path('deleteUser/<delId>', views.deleteUser, name = "deleteUser"),
    path('updateUser/<pk>', views.updateUser, name = "updateUser"),
    path('insertTopic/', views.insertTopic, name = "insertTopic"),
    path('manageTopics/', views.manageTopics, name = "manageTopics"),
    path('deleteTopic/<delId>', views.deleteTopic, name = "deleteTopic"),
]