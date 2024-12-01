from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.registerPage, name = "register"),

    path('', views.home, name = "home"),
    path('room/<str:pk>/', views.room, name = "room"),
    path('profile/<str:pk>/', views.userProfile, name = "user-profile"),
    
    path('create-room/', views.createRoom, name = "create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name = "update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name = "delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name = "delete-message"),

    path('update-user/', views.updateUser, name = "update-user"),
    path('topics/', views.topicsPage, name = "topics"),
    path('activity/', views.activitiyPage, name = "activity"),
    path('forgotPass/', views.forgotPass, name = "forgotPass"),
    path('varifyOTP/', views.varifyOTP, name = "varifyOTP"),
    path('resendOTP/', views.resendOTP, name = "resendOTP"),
    path('resetPass/', views.resetPass, name = "resetPass"),
    path('item/<int:item_id>/like/', views.like_item, name='like-item'),
]