from django.urls import path
from . import views

# This maps url request to a view handler

# This stores all url requests with its views respose
urlpatterns = [
    # path( url given, reponse from views )
    # Note: Always end urls with /
    path('', views.home_page, name = "home"), 
    path('topic/', views.topics_page, name = "topics"), 
    path('activity/', views.activity_page, name = "activity_feed"), 

    path('login/', views.login_page, name = "login"),
    path('logout/', views.logout_user, name = "logout"),
    path('register/', views.register_page, name = "register"),

    path('profile/<str:pk>', views.profile, name = "profile"),
    path('upadte-profile', views.update_profile, name = "update_profile"),

    path('room/<str:pk>/', views.room_page, name = "room"),
    path('create-room/', views.room_form, name = "room_form"),
    path('update-room/<str:pk>/', views.update_room, name = "update_room"),
    path('delete-room/<str:pk>/', views.delete_room, name = "delete_room"),

    path('create-topic/', views.topic_form, name = "topic_form"),
    path('update-topic/<str:pk>/', views.update_topic, name = "update_topic"),
    path('delete-topic/<str:pk>/', views.delete_topic, name = "delete_topic"),

    path('update-message/<str:pk>/', views.update_message, name = "update_message"),
    path('delete-message/<str:pk>/', views.delete_message, name = "delete_message")
]